#!/usr/bin/python
# This program is created by Skye

import os

from cryptography.fernet import Fernet

# Set the base directory depending on the operating system
base = "c:\\" if os.name == 'nt' else "/root"

# Read the encryption key from the provided file location
with open(input("Enter your key file location: "), 'rb') as fl:
    key = fl.read()  # No need to encode as it's already in bytes

# Function to decrypt files


def decrypt(key, file):
    try:
        # Read the encrypted file
        with open(file, 'rb') as f:
            data = f.read()

        # Decrypt the file content
        fernet = Fernet(key)
        decrypted = fernet.decrypt(data)

        # Create the decrypted file (removing ".encrypted" extension)
        # Removes the last 10 characters, i.e., ".encrypted"
        decrypted_file = file[:-10]

        # Write the decrypted content back to a new file
        with open(decrypted_file, 'wb') as f:
            f.write(decrypted)

        # Remove the encrypted file
        os.remove(file)
        print(f"[+] Decrypted and removed: {file}")

    except Exception as e:
        print(f"[-] Error decrypting {file}: {e}")

# Function to list files and decrypt those ending with ".encrypted"


def filelist():
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(".encrypted"):
                fpath = os.path.join(root, file)
                print(f"Decrypting {fpath}...")
                decrypt(key, fpath)


# Execute the file listing and decryption
filelist()
