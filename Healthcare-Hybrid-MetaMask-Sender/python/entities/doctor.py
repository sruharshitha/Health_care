import socket
from crypto.ecdh import generate_keypair
from crypto.kdf import derive_session_key
from crypto.aes256 import encrypt_message
from config import RECEIVER_IP, PORT

print("Doctor system started")

s = socket.socket()

s.connect((RECEIVER_IP, PORT))

print("Verifying Robot")

s.send(b"doctor")

response = s.recv(1024)

if response != b"robot_ok":
    print("Robot verification failed")
    exit()

print("Robot verified")

private, public = generate_keypair()

s.send(str(public).encode())

robot_public = int(s.recv(1024).decode())

session_key = derive_session_key(private, robot_public)

print("Session key generated")

message = input("Enter message: ")

encrypted = encrypt_message(message, session_key)

s.send(encrypted)

print("Encrypted message sent")