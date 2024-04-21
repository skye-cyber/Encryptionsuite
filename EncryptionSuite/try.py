from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64


# generate encryption key for the file using a passphrase
def generate_enc_key(passphrase):
    salt = b'salt_'  # Add a salt for added security
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,  # Adjust the number of iterations as needed for security
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
    cipher = Fernet(key)
    print(f"\033[1;32m{key}\033[0m")
    print(f"\033[1;32m{cipher}\033[0m")


generate_enc_key("skyedddddd")
