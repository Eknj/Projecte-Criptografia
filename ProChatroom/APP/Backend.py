from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
import random
import math

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

rooms = {}
room_rsa_keys = {}

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def mod_inverse(e, fi):
    for d in range(3, fi):
        if (d * e) % fi == 1:
            return d
    raise ValueError("mod_inverse does not exist")

def generate_key_pair():
    p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)

    while p == q:
        q = generate_prime(1000, 5000)

    n = p * q
    fi_n = (p - 1) * (q - 1)

    e = random.randint(3, fi_n - 1)
    while math.gcd(e, fi_n) != 1:
        e = random.randint(3, fi_n - 1)

    d = mod_inverse(e, fi_n)
    
    print(f"Public key (n, e): ({n}, {e})")
    print(f"Private key (n, d): ({n}, {d})")

    return n, e

def encrypt_rsa(message, public_key):
    n, e = public_key
    message_ascii = [ord(ch) for ch in message]
    ciphertext = [pow(ch, e, n) for ch in message_ascii]
    return ciphertext

def decrypt_rsa(ciphertext, private_key):
    n, d = private_key
    decrypted_ascii = [pow(ch, d, n) for ch in ciphertext]
    decrypted_message = "".join(chr(ch) for ch in decrypted_ascii)
    return decrypted_message

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        if code not in rooms:
            break

    return code

@app.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
            # Generate RSA keys for the room
            room_rsa_keys[room] = generate_key_pair()
        elif code not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("home.html")

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("home"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return

    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    # Encrypt the message using RSA before sending
    public_key = room_rsa_keys.get(room, None)
    if public_key:
        encrypted_message = encrypt_rsa(content["message"], public_key)
        content["message"] = encrypted_message

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]

    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == "__main__":
    socketio.run(app, debug=True)
