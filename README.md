# Projecte-Criptografia
Final Chriptography project

## Overview

This repository contains a simple chat application built using Flask and Flask-SocketIO. The application incorporates RSA encryption to secure the messages exchanged between users within a chat room. The encryption keys are generated dynamically for each chat room to enhance security.

## Features

1. **Secure Chat Communication:**
   - The chat messages exchanged within a room are encrypted using a personalized RSA encryption algorithm.
   - Each chat room has a unique pair of public and private keys generated dynamically.

2. **Dynamic Room Creation:**
   - Users can create new chat rooms by providing a unique name.
   - Each room is associated with a unique RSA key pair for message encryption.

3. **Joining Existing Rooms:**
   - Users can join existing chat rooms by entering the room code.
   - The application ensures that users cannot join non-existing rooms.

4. **Real-time Updates:**
   - Chat messages are updated in real-time using Flask-SocketIO for a seamless user experience.

5. **Server Prints Window:**
   - The application includes a server prints window that displays server-side logs and activities in real-time.

## Disclamer

This project incorporates code or components from the following GitHub projects. All credit and acknowledgment for their contributions go to the respective authors:

- [Python-Live-Chat-App](https://github.com/techwithtim/Python-Live-Chat-App):
Uses Flask Sockets to create a live chat room application.

- I watched his tutorial and used it as a base for my project later on i'm gonna show the main diferences.

## Used Libraries
 
This project relies on the following libraries to implement its features:

- [Flask](https://flask.palletsprojects.com/): A lightweight web application framework.
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/): A Flask extension for handling WebSocket connections.
- [Tkinter](https://docs.python.org/3/library/tkinter.html): The standard Python interface to the Tk GUI toolkit.
- [Random](https://docs.python.org/3/library/random.html): Python's built-in library for generating random numbers.
- [Math](https://docs.python.org/3/library/math.html): Python's built-in library for mathematical functions.
- [Threading](https://docs.python.org/3/library/threading.html): Python's built-in library for working with threads, allowing concurrent execution of tasks.
- [Sys](https://docs.python.org/3/library/sys.html): Python's built-in module providing access to some variables used or maintained by the Python interpreter.

## RSA Function Explanations

#### `is_prime(n, k=5)`

Determines if a number `n` is prime using the Fermat primality test with `k` iterations. It returns `True` if `n` is prime; otherwise, it returns `False`.

#### `generate_prime(min_value, max_value)`

Generates a random prime number between the specified `min_value` and `max_value` using the `is_prime` function.

#### `extended_gcd(a, b)`

Computes the extended Euclidean algorithm to find the greatest common divisor (`d`) of `a` and `b`, along with coefficients `x` and `y` such that `ax + by = d`.

#### `mod_inverse(e, fi)`

Calculates the modular inverse of `e` modulo `fi` using the extended Euclidean algorithm. Raises a `ValueError` if the modular inverse does not exist.

#### `generate_key_pair()`

Generates a pair of RSA public and private keys (`n`, `e`) and (`n`, `d`) using random prime numbers. It also prints the generated keys and returns them.

#### `encrypt_rsa(message, public_key)`

Encrypts a text message using RSA encryption with the provided public key (`n`, `e`). Converts each character to its ASCII representation and performs modular exponentiation.

#### `mod_exp(base, exponent, modulus)`

Implements modular exponentiation efficiently using the square-and-multiply algorithm.

#### `decrypt_rsa(ciphertext, private_key)`

Decrypts an RSA-encrypted ciphertext using the provided private key (`n`, `d`). Utilizes modular exponentiation to retrieve the original message.

#### `generate_unique_code(length)`

Generates a unique code of the specified `length` composed of uppercase letters. Ensures the generated code is not already in use within the application's chat rooms.

For a more in-depth understanding, please refer to the source code for each function.

## USAGE
