import base64

# import subprocess
import logging
import logging.handlers
import os
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .colors import (
    BWHITE,
    DMAGENTA,
    FMAGENTA,
    MAGENTA,
    RED,
    RESET,
    DBLUE,
    CGREEN,
    CYAN,
    DCYAN,
)

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logger = logging.getLogger(__name__)


class HandleFiles:
    def __init__(self, input_file, passphrase):
        self.input_file = input_file
        self.passphrase = passphrase

    # generate encryption key for the file using a passphrase
    @staticmethod
    def generate_enc_key(passphrase):
        try:
            # Add a salt for added security
            salt = salt = (
                b"_dfjrf7404dxhdhcbvxzxt2423839e7wxcv(lkhdamet38i839ebncdggdee-/_"
            )
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA512(),
                length=32,
                salt=salt,
                iterations=1_000_000,  # Adjust the number of iterations as needed for security
                backend=default_backend(),
            )
            key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
            return key
        except Exception as e:
            print(f"{RED}{e}{RESET}")

    # function to read and encrypt the file
    def levelOkay(self, path):
        level = path[-1:]

        if level.isdigit() and int(level) >= 3 and path[:-1].endswith(".enc"):
            sys.exit(f"{RED}Reached maximum encryption levels{RESET}")

    def encrypt_file(self, status: bool = True):
        original_path = self.input_file
        self.levelOkay(original_path)

        try:
            # Read original file
            with open(original_path, "rb") as file:
                data = file.read()

            # Generate key and encrypt
            key = HandleFiles.generate_enc_key(self.passphrase)
            cipher = Fernet(key)
            encrypted_data = cipher.encrypt(data)

            # Determine encryption level
            filename = os.path.basename(original_path)
            dirname = os.path.dirname(original_path)

            if filename.endswith(".enc") and filename[-5:-4].isdigit():
                level = int(filename[-5:-4])  # .enc0, .enc1
                base_name = filename[:-5]
            elif filename[-1:].isdigit() and filename[-6:-3] == ".enc":
                level = int(filename[-1:])
                base_name = filename[:-6]
            else:
                level = -1
                base_name = filename

            new_level = level + 1
            output_filename = f"{base_name}.enc{new_level}"
            output_file = os.path.join(dirname, output_filename)

            # Write encrypted file
            with open(output_file, "wb") as file:
                file.write(encrypted_data)

            print(f"{CGREEN}Saved as{RESET} {output_file}")
            status = False

        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)

        except Exception as e:
            logger.error(f"{BWHITE}{e}{RESET}")
            sys.exit(1)

        self.encCleanup(original_path, status)

        return output_file

    def encCleanup(self, original_path, status):
        # Cleanup logic after encryption
        if not status:
            try:
                os.remove(original_path)
                print(f"{FMAGENTA}Deleted original: {BWHITE}{original_path} 🚮{RESET}")
            except Exception as e:
                logger.warning(f"Could not delete {original_path}: {e}")
        else:
            print(f"{RED}Encryption failure.{RESET}")

    def decrypt_file(self, status: bool = True):
        encrypted_path = self.input_file

        try:
            # Generate key and decryptor
            key = HandleFiles.generate_enc_key(self.passphrase)
            cipher = Fernet(key)

            # Read encrypted file
            with open(encrypted_path, "rb") as file:
                encrypted_data = file.read()

            decrypted_data = cipher.decrypt(encrypted_data)

            print(f"{DCYAN}Restoring file name...{RESET}")

            # Determine decryption level
            filename = os.path.basename(encrypted_path)
            dirname = os.path.dirname(encrypted_path)

            # Match pattern: filename.ext.encN
            if filename[-1:].isdigit() and filename[-5:-1] == ".enc":
                level = int(filename[-1:])
                base_name = filename[:-5]
            else:
                print(f"{RED}Invalid encrypted file name format.{RESET}")
                return None

            # Decide output file name
            if level > 0:
                output_filename = f"{base_name}.enc{level - 1}"
            else:
                output_filename = base_name

            output_file = os.path.join(dirname, output_filename)

            # Write decrypted data
            with open(output_file, "wb") as file:
                file.write(decrypted_data)

            logger.info(f"{CGREEN}Saved as:{RESET} {BWHITE}{output_file}{RESET}")
            status = False

        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)

        except Exception as e:
            print(f"{RED}Decryption failed: {e}{RESET}")

        # Post-decryption cleanup
        self.decClean(encrypted_path, status)

        return output_file if not status else None

    def decClean(self, encrypted_path, status):
        if not status:
            try:
                os.remove(encrypted_path)
                print(
                    f"{FMAGENTA}Deleted encrypted: {BWHITE}{encrypted_path} 🚮{RESET}"
                )
            except Exception as e:
                logger.warning(f"Could not delete {encrypted_path}: {e}")
        else:
            print(f"{RED}Decryption failure.{RESET}")


class HandleFolders:
    def __init__(self, folder, passphrase):
        self.passphrase = passphrase
        self.folder = folder

        print(f"{DCYAN}Root directory{RESET} = {CGREEN}{self.folder}{RESET}")

    def encrypt_folder(self):
        try:
            # Iterate over all files in the folder
            for root, dirs, files in os.walk(self.folder):
                for file in files:
                    input_file = os.path.join(root, file)

                    print(f"{DBLUE}Encrypt{MAGENTA} {file}{RESET}")

                    init = HandleFiles(input_file, self.passphrase)
                    init.encrypt_file()

        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)

        except Exception as e:
            raise
            print(f"Sorry:: {BWHITE}{e}{RESET}")

    def decrypt_folder(self):
        try:
            # Iterate over all files in the folder
            for root, dirs, files in os.walk(self.folder):
                for file in files:
                    if file[-4:-1] == "enc":
                        input_file = os.path.join(root, file)
                        print(f"{DCYAN}Decrypt {MAGENTA}{file}{RESET}", end="\n")

                        init = HandleFiles(input_file, self.passphrase)
                        init.decrypt_file()

                    input_file = os.path.join(root, file)

                    if os.path.isfile(input_file) and input_file[-4:-1] != "enc":
                        print(
                            f"{BWHITE}The file {CYAN}{input_file}{RESET}{BWHITE} doesn't appear to be encrypted{RESET}"
                        )
                        pass
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)

        except Exception as e:
            print(f"Sorry:: {BWHITE}{e}{RESET}")


if __name__ == "__main__":
    init = HandleFiles("test.docx", "skye")
    init.encrypt_file()
