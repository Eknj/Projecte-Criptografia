from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from rsadefs import *
import threading
import tkinter as tk
import sys

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)
rooms = {}
room_rsa_keys = {}

class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, text):
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", text)
        self.text_widget.configure(state="disabled")
        self.text_widget.see("end")

    def flush(self):
        pass

class ServerPrintsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Server Prints")
        self.geometry("600x400")

        self.text_widget = tk.Text(self, wrap="word", state="disabled")
        self.text_widget.pack(expand=True, fill="both")

        sys.stdout = TextRedirector(self.text_widget)

        self.room_listbox = tk.Listbox(self, selectmode=tk.SINGLE)
        self.room_listbox.pack()

        self.room_code_entry = tk.Entry(self)
        self.room_code_entry.pack()

        join_button = tk.Button(self, text="Join Room", command=self.join_room)
        join_button.pack()

        self.update_room_list()

    def join_room(self):
        selected_index = self.room_listbox.curselection()
        if selected_index:
            selected_room = self.room_listbox.get(selected_index)
            self.display_room(selected_room)
        else:
            room_code = self.room_code_entry.get()
            if room_code:
                self.display_room(room_code)

    def display_room(self, room):
        session.clear()
        session["room"] = room
        room_window = RoomWindow(self, room)
        room_window.mainloop()

    def update_room_list(self):
        available_rooms = list(rooms.keys())
        self.room_listbox.delete(0, tk.END)
        for room in available_rooms:
            self.room_listbox.insert(tk.END, room)

class RoomWindow(tk.Toplevel):
    def __init__(self, master, room):
        super().__init__(master)
        self.title(f"Room: {room}")
        self.geometry("400x300")
        self.text_widget = tk.Text(self, wrap="word", state="disabled")
        self.text_widget.pack(expand=True, fill="both")

def run_tkinter():
    server_prints_window = ServerPrintsWindow()
    server_prints_window.mainloop()

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
    public_key = room_rsa_keys.get(room, None)
    private_key = room_rsa_keys.get(room, None)
    if public_key:
        encrypted_message = encrypt_rsa(content["message"], public_key)
        content["message"] = encrypted_message
        dectypted_message = decrypt_rsa(encrypted_message, private_key) 
    send(content, to=room)
    rooms[room]["messages"].append(content)
    #print(f"{session.get('name')} said: {dectypted_message}")
    print(f"{session.get('name')} said: {data["data"]}")

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
    tkinter_thread = threading.Thread(target=run_tkinter)
    tkinter_thread.daemon = True
    tkinter_thread.start()
    socketio.run(app, debug=True)
