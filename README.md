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


