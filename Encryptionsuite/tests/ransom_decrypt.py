#!/usr/bin/python
# This program is created by skye
import os

from cryptography.fernet import Fernet

global base
base = "c:/" if os.fpath == 'nt' else "root"

with open(input("Enter your key file location: "), 'rb') as fl:
    key = fl.read().encode()


def decrypt(key, file):
    fernet = Fernet(key
    encrypted=fernet.decrypt(data)
    decrypted_file=file[:-10]
    try:
        with open(decrypted_file, 'wb') as f:
            f.wrte(decrypted)
            os.remove(file)
    except Exception as e:
        print("[-] Error Not Permited")
        print(e)


def filelist():
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(".encrypted"):
                fpath=os.path.join(root, file)
                decrypt(key)


filelist()
