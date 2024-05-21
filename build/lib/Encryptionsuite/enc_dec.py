import os
import sys
import subprocess
from cryptography.fernet import Fernet
import logging
import logging.handlers

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


# generate encryption key for the file
class KeyGen:

    def __init__(self):
        self = self

    def generate_random_enc_key():
        try:
            return Fernet.generate_key()
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.info(f"{e}")


# function to read and encrypt the file
def encrypt_file(file_path, ocipher=None):
    # join to form new new output_file
    # file_path = input_file
    try:

        key = KeyGen.generate_random_enc_key()
        cipher = Fernet(key)
        # save the key in a key file
        try:
            key_string = key.decode()
            logger.info(f"Generated key::> {key_string}\n")
            # extract input_file basename
            basename, extension = os.path.splitext(file_path)
            keyfile = basename + '.xml'
            with open(keyfile, 'x', newline='\r\n') as file:
                logger.info(f"Saving the key to \033[34m{file.name}\033[0m")
                file.write(key_string)
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.error(f'\033[31m{e}\033[0m')
        # open the file for encryption
        with open(file_path, 'rb') as file:
            data = file.read()

        # print(f"Comencing encrption process{show_loading_dots()}")
        encrypted_data = cipher.encrypt(data)

        # Append '.enc' to the file name
        enc_file_path = file_path + '.enc'
        # write out encrypted file data to a new file
        with open(enc_file_path, 'wb') as file:
            file.write(encrypted_data)

            # remove/permanently delete inpu file
            subprocess.run(['rm', f'{file_path}'])

        key_string = key.decode()
        logger.info(
            f"{file_path} encrypted successfully with key=\033[32m{key_string}\033[0m")
        output_file = enc_file_path
    except KeyboardInterrupt:
        print("\nExiting")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\033[31m{e}\033[0m")
    return output_file


def decrypt_file(encrypted_file_path, key):
    try:
        # search for encryption key in default key file
        if key == 'file':
            try:
                basename, ext1 = os.path.splitext(encrypted_file_path)
                final_basename, ext2 = os.path.splitext(basename)

                default_key_file = final_basename + '.xml'
                logger.info(f"Searching for key in {default_key_file}")

                # where default_key_file has only one extension
                # final_basename, ext1 = os.path.splitext(encrypted_file_path)

                if os.path.exists(default_key_file):
                    try:
                        with open(default_key_file, 'r') as file:
                            key = file.read()
                            logger.info(f"Using key from {default_key_file}")
                        return key
                    except FileNotFoundError:
                        logger.error(
                            f"\033[31m{default_key_file} not found\033[0m")
                        return
                else:
                    logger.error(
                        f"\033[31m{default_key_file} not found\033[0m")
                return
            except KeyboardInterrupt:
                print("\nExiting")
                sys.exit(1)
            except Exception:
                pass

        elif os.path.isfile(key):
            with open(key, 'r') as file:
                key = file.read()
            return key

    finally:
        # Ensure the key is of type bytes
        key = key.encode() if isinstance(key, str) else key
        cipher = Fernet(key)

        # open the file for decryption
        with open(encrypted_file_path, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        # Removing '.encrypted from the file name
        with open(encrypted_file_path[:-4], 'wb') as file:
            file.write(decrypted_data)
        logger.info(
            f"{encrypted_file_path} decrypted successfully with key=\033[32m{key.decode()}\033[0m")
    # except Exception as e:
    # print(f"\033[31m{e}\033[0m")


def encrypt_folder(folder_path):
    try:
        # Iterate over all files in the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                encrypt_file(file_path)
    except KeyboardInterrupt:
        print("\nExiting")
        sys.exit(1)
    except Exception as e:
        print(f"Sorry:: \033[31m{e}\033[0m")


def decrypt_folder(encrypted_folder_path, key):
    try:
        # Iterate over all files in the folder
        for root, dirs, files in os.walk(encrypted_folder_path):
            for file in files:
                encrypted_folder_path = os.path.join(root, file)
                decrypt_file(encrypted_folder_path, key)
    except KeyboardInterrupt:
        print("\nExiting")
        sys.exit(1)
    except Exception as e:
        print(f"Sorry:: \033[31m{e}\033[0m")
