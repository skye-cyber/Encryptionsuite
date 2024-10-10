import os
from cryptography.fernet import Fernet


def encrypt_file(file_path, key):
    # Read the contents of the file
    with open(file_path, 'rb') as file:
        file_data = file.read()

    # Create a Fernet cipher object with the provided key
    cipher = Fernet(key)

    # Encrypt the file data
    encrypted_data = cipher.encrypt(file_data)

    # Write the encrypted data back to the file
    with open(file_path, 'wb') as file:
        file.write(encrypted_data)


def encrypt_folder(folder_path, key):
    # Iterate over all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)


# Generate a key
key = Fernet.generate_key()

# Path to the folder you want to encrypt
folder_path = 'path/to/your/folder'

# Encrypt the files within the folder
encrypt_folder(folder_path, key)
