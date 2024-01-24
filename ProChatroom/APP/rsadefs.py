import random
import math
from Backend import rooms

def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    # Realitzar el test de primalitat de Fermat k vegades
    for _ in range(k):
        a = random.randint(2, n - 2)
        if pow(a, n - 1, n) != 1:
            return False
    return True


def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):
        prime = random.randint(min_value, max_value)
    return prime

def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = extended_gcd(b, a % b)
        return d, y, x - y * (a // b)

def mod_inverse(e, fi):
    d, x, _ = extended_gcd(e, fi)
    if d == 1:
        return x % fi
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
    message_ascii = [ord(char) for char in message]
    aa = [str(integer) for integer in message_ascii]
    bb = "".join(aa)
    vv = int(bb)
    ciphertext = mod_exp(vv, e, n)
    return ciphertext

def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus

    while exponent > 0:
        
        if exponent % 2 == 1:
            result = (result * base) % modulus
            
        exponent //= 2
        base = (base * base) % modulus

    return result

def decrypt_rsa(ciphertext, private_key):
    n, d = private_key
    first_decrypt = mod_exp(ciphertext, d, n)
    cc = str(first_decrypt)
    llista = [int(digit) for digit in cc]
    decrypted_message = [chr(eee) for eee in llista]
    
    return decrypted_message

def generate_unique_code(length):
    while True:
        code = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(length))
        if code not in rooms:
            break
    return code