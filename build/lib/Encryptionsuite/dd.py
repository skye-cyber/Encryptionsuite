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

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

# import pyperclip


class HandleFiles:

    def __init__(self, input_file, passphrase):
        self.input_file = input_file
        self.passphrase = passphrase

    # generate encryption key for the file using a passphrase
    @staticmethod
    def generate_enc_key(passphrase):
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
            # print("\033[1;35mRestore file name\033[0m")
            e_level = int(file[-1:]) - 1 if file[-4:-
                                                 1] == 'enc' and int(file[-1:]) != 0 else ''
            fname = f'{file[:-1]}{e_level}' if e_level != '' else file[:-5]
            with open(fname, 'wb') as file:
                file.write(decrypted_data)

                # _out_ = f'{self.input_file[:-1]}{int(self.input_file[-1:]) -1}' if int(self.input_file[-1:]) != 0 else f'{self.input_file[:-1]}{int(self.input_file[-1:])}'

            # logger.info(
              #  f"\033[1m File Decrypted successfully as \033[1m{fname}\033[0m")

        except KeyboardInterrupt:
            print("\nQuit!")
            sys.exit(1)

        except Exception as e:
            print(f"\033[31m{e}\033[0m",end='\r')
        if os.path.exists(_path_[:-1] + f'{0}') or os.path.exists(_path_[:-1] + f'{1}') or os.path.exists(_path_[:-1] + f'{2}'):
            if status is True:
                print("\033[31mDecryption failure.\033[0m\n")

        elif os.path.exists(_path_[:-1] + f'{0}') or os.path.exists(_path_[:-1] + f'{1}') or os.path.exists(_path_[:-1] + f'{2}'):
            print(f"\033[2;35mDelete \033[1m{_path_}🚮\033[0m")
            os.remove(_path_)


class Bruteforce:
    def __init__(self, obj, dict_file):
        self.obj = obj
        self.dict_file = dict_file

    def conservative(self):
        # Critical redundacy
        # Goal:-> Is to avoid loosing the original files by Creating temporary directory to store temporary files
        if os.path.isfile(self.obj):
            _file = os.path.split(self.obj)[-1]
            _path = os.path.dirname(self.obj)
            _dir = os.path.join(_path, "CRDIR")
            # Create temporary directory
            if not os.path.exists(_dir):
                os.mkdir(_dir)
            cmd = f"cp {self.obj} {_dir}"
            os.system(cmd)
            # Call file bruteforce function function
            _fpath = os.path.join(_dir, _file)

            # Open dictionary file for Bruteforce
            with open(self.dict_file, 'r') as df:
                passw = df.readlines()
            # passw = list(passw)
            # pass_ls = ['hello', "pass", "password", "passrr", "hhhh"]
            try:
                for key in passw:
                    # key = key.strip('\n'
                    print(f"\033[1;30m{key}\033[0m", end='\r')
                    # Create decryption object
                    init = HandleFiles(_fpath, key)
                    init.decrypt_file(False)
            except BaseException as e:
                print(e)


init = Bruteforce("/home/skye/Documents/AReport.docx.enc0",
                  "/home/skye/Documents/john.lst")
init.conservative()
