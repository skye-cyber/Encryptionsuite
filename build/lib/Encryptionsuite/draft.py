from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
import os


def generate_keys(password, salt):
    kdf = PBKDF2(password, salt, dkLen=32, count=100000,
                 hmac_hash_module=SHA256())
    private_key = RSA.generate(public_exponent=65537, key_size=2048)
    public_key = private_key.publickey()
    return private_key, public_key, kdf.compute_der()


def encrypt_file(private_key, file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    cipher = PKCS1_OAEP()
    ciphertext = private_key.sign(data, cipher)
    with open(file_path, 'wb') as f:
        f.write(ciphertext)


def decrypt_file(public_key, file_path):
    with open(file_path, 'rb') as f:
        ciphertext = f.read()

    plaintext = public_key.verify(ciphertext)
    with open(file_path, 'wb') as f:
        f.write(plaintext)


if __name__ == '__main__':
    private_key, public_key, derived_secret = generate_keys(
        "your_password", os.urandom(16))
    encrypt_file(private_key, "your_file_path")
    decrypt_file(public_key, "your_file_path")
