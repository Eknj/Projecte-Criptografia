import random
import math

def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True

def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = gcd_extended(b % a, a)
        return gcd, y - (b // a) * x, x

def mod_inverse(e, fi):
    gcd, x, _ = gcd_extended(e, fi)
    if gcd != 1:
        raise ValueError("mod_inverse does not exist")
    else:
        return x % fi

# Generate random prime numbers p and q
p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)

# Ensure p and q are distinct
while p == q:
    q = generate_prime(1000, 5000)

n = p * q
fi_n = (p - 1) * (q - 1)

# Generate random public exponent (e) and calculate private exponent (d)
e = generate_prime(2, fi_n - 1)
d = mod_inverse(e, fi_n)

print("Public Key (e):", e)
print("Private Key (d):", d)
print("n:", n)
print("Totient (fi_n):", fi_n)
print("p:", p)
print("q:", q)

# Encrypt a message
message = input("Raw Message: ")
message_ascii = [ord(ch) for ch in message]
ciphertext = [pow(ch, e, n) for ch in message_ascii]

# Interactive decryption with password
password = int(input("Enter password to decrypt: "))

if password == d:
    decrypted_ascii = [pow(ch, d, n) for ch in ciphertext]
    decrypted_message = "".join(chr(ch) for ch in decrypted_ascii)
    print("Decrypted Message:", decrypted_message)
else:
    print("Encrypted Message:", ciphertext)

