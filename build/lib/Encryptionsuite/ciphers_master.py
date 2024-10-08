import subprocess
from mciphers import caesar_cipher


class ciphers_HandleFiles:

    def __init__(self, input_file, passphrase, cipher):
        self.passphrase = passphrase
        self.input_file = input_file
        self.cipher = cipher

    # function to read and encrypt the file
    def encrypt_file(self):
        try:

            # open the file for encryption
            with open(self.input_file, 'rb') as file:
                data = file.read()

            print("\033[1;32mComencing encryption process\033[0m")
            encrypted_data = cipher.encrypt(data)

            # Append '.encrypted' to the file name
            print("\033[1;35mModifying file name\033[0m")
            output_file = self.input_file + '.enc'

            # write out encrypted file data to a new file
            with open(output_file, 'wb') as file:
                file.write(encrypted_data)

                # remove/permanently delete input_file
                subprocess.run(['rm', '-r', f'{self.input_file}'])

            logger.info(
                f"{self.input_file} encrypted successfully with key=\033[36m{self.passphrase}\033[0m")

            print("\033[1;32mDone\033[0m")
            print(f"File saved as {output_file}")
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.error(f"\033[31m{e}\033[0m")
        return output_file

    def decrypt_file(self):
        print("\033[1;33mComencing decryption process\033[0m")
        try:
            # Ensure the key is of type bytes
            init = PassKeyGen(self.passphrase)
            key = init.generate_enc_key()
            cipher = Fernet(key)

            # open the file for decryption
            with open(self.input_file, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = cipher.decrypt(encrypted_data)

            # Removing '.encrypted from the file name
            with open(self.input_file[:-4], 'wb') as file:
                file.write(decrypted_data)
            print("\033[1;32mDone\033[0m")
            logger.info(
                f"{self.input_file} decrypted successfully as {self.input_file} with key=\033[32m{self.passphrase}\033[0m")
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            print(f"\033[31m{e}\033[0m")


class HandleFolders:
    def __init__(self, folder, passphrase):
        self.passphrase = passphrase
        self.folder = folder

    def encrypt_folder(self):
        try:
            # Iterate over all files in the folder
            for root, dirs, files in os.walk(self.folder):
                for file in files:
                    input_file = os.path.join(root, file)
                    print(f"\033[1;34mEncrypting{input_file}\033[0m", end="\r")
                    init = HandleFiles(input_file, self.passphrase)
                    init.encrypt_file()
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            print(f"Sorry:: \033[31m{e}\033[0m")

    def decrypt_folder(self):
        try:
            # Iterate over all files in the folder
            for root, dirs, files in os.walk(self.folder):
                for file in files:
                    if file.endswith(".enc"):
                        input_file = os.path.join(root, file)
                        print(
                            f"\033[1;34mDecrypting{input_file}\033[0m", end="\r")
                        init = HandleFiles(input_file, self.passphrase)
                        init.decrypt_file()
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            print(f"Sorry:: \033[31m{e}\033[0m")
