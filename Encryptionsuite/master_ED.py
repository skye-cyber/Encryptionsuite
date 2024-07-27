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

from .colors import (BWHITE, DMAGENTA, FMAGENTA, MAGENTA, RED,
                     RESET, DBLUE, CGREEN, CYAN, DCYAN, CGREEN)

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
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
            salt = salt = b'_dfjrf7404dxhdhcbvxzxt2423839e7wxcv(lkhdamet38i839ebncdggdee-/_'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA512(),
                length=32,
                salt=salt,
                iterations=1_000_000,  # Adjust the number of iterations as needed for security
                backend=default_backend()
            )
            key = base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))
            return key
        except Exception as e:
            print(f"{RED}{e}{RESET}")

    # function to read and encrypt the file
    def encrypt_file(self, status: bool = True):
        _path_ = self.input_file
        # logger.info(f"{BWHITE}@key=\033[30m{self.passphrase}{RESET}")
        try:

            # open the file for encryption
            with open(self.input_file, 'rb') as file:
                data = file.read()

            key = HandleFiles.generate_enc_key(self.passphrase)
            cipher = Fernet(key)
            encrypted_data = cipher.encrypt(data)

            # Append '.enc{e_level}' to the file name
            print(F"{DMAGENTA}Modifying file name{RESET}")

            file = self.input_file
            e_level = int(file[-1:]) + 1 if file[-4:-1] == 'enc' else 0
            output_file = f'{file[:-1]}{e_level}' if file[-4:-
                                                          1] == 'enc' else f'{file}.enc{e_level}'

            # write out encrypted file data to a new file
            with open(output_file, 'wb') as file:
                file.write(encrypted_data)

                # remove/permanently delete input_file
                # subprocess.run(['rm', '-r', f'{self.input_file}'])

            # logger.info(f"{BWHITE}{self.input_file}{RESET} encrypted successfully")

            print(f"{CGREEN}Saved as{RESET} {output_file}")
            status = False

        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)

        except Exception as e:
            logger.error(f"{BWHITE}{e}{RESET}")
            sys.exit(1)

        if status is True and (not os.path.exists(_path_ + f'.enc{0}') or os.path.exists(_path_ + f'.enc{1}')):
            print(f"{RED}Encryption failure.{RESET}")

        elif status is False and (os.path.exists(_path_ + f'.enc{0}') or os.path.exists(_path_ + f'.enc{1}')):
            print(f"{FMAGENTA}Delete {BWHITE}{_path_}🚮{RESET}")
            os.remove(_path_)

        return output_file

    def decrypt_file(self, status: bool = True):
        _path_ = self.input_file

        try:
            # Ensure the key is of type bytes
            key = HandleFiles.generate_enc_key(self.passphrase)
            cipher = Fernet(key)

            # open the file for decryption
            with open(self.input_file, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = cipher.decrypt(encrypted_data)

            # Extract encryption infor from the encrypted file for decide on appropriate file name
            file = self.input_file

            print(f"{DCYAN}Restore file name{RESET}")

            e_level = int(file[-1:]) - 1 if file[-4:-
                                                 1] == 'enc' and int(file[-1:]) != 0 else ''
            fname = f'{file[:-1]}{e_level}' if e_level != '' else file[:-5]

            with open(fname, 'wb') as file:
                file.write(decrypted_data)

                # _out_ = f'{self.input_file[:-1]}{int(self.input_file[-1:]) -1}' if int(self.input_file[-1:]) != 0 else f'{self.input_file[:-1]}{int(self.input_file[-1:])}'

            logger.info(
                f"{CGREEN} Save as:{RESET} {BWHITE}{fname}{RESET}")
            status = False

        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)

        except BaseException as e:
            print(f"{RED}{e}{RESET}")

        except Exception as e:
            print(f"{BWHITE}{e}{RESET}")

        # and (not os.path.exists(_path_[:-1] + f'{0}') or os.path.exists(_path_[:-1] + f'{1}') or os.path.exists(_path_[:-1] + f'{2}')):
        if status is True:
            print(f"{RED}Decryption failure.{RESET}")

        elif status is False and (os.path.exists(_path_[:-1] + f'{0}') or os.path.exists(_path_[:-1] + f'{1}') or os.path.exists(_path_[:-1] + f'{2}')):
            print(f"{FMAGENTA}Delete {BWHITE}{_path_}🚮{RESET}")
            os.remove(_path_)


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
            print(f"Sorry:: {BWHITE}{e}{RESET}")

    def decrypt_folder(self):
        try:
            # Iterate over all files in the folder
            for root, dirs, files in os.walk(self.folder):

                for file in files:

                    if file[-4:-1] == "enc":

                        input_file = os.path.join(root, file)
                        print(
                            f"{DCYAN}Decrypt {MAGENTA}{file}{RESET}", end='\n')

                        init = HandleFiles(input_file, self.passphrase)
                        init.decrypt_file()

                    input_file = os.path.join(root, file)

                    if os.path.isfile(input_file) and input_file[-4:-1] != "enc":
                        print(
                            f"{BWHITE}The file {CYAN}{input_file}{RESET}{BWHITE} doesn't appear to be encrypted{RESET}")
                        pass
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)

        except Exception as e:
            print(f"Sorry:: {BWHITE}{e}{RESET}")


if __name__ == "__main__":
    init = HandleFiles('test.docx', 'skye')
    init.encrypt_file()
