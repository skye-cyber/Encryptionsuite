# import re
import os
import sys
import logging
import logging.handlers

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

# Define the Caesar cipher class


class CaesarCipher:
    def __init__(self, message, key=8):
        """Initialize the Caesar Cipher object."""
        self.message = message
        self.key = key
        # print(message)

    def encode(self):
        """Encode the given message using the provided key."""
        # print(self.message)
        result = ''
        for char in self.message:
            if char.isalpha():
                # Shift the character by the given key
                shifted_value = ord(char) + self.key
                # Handle uppercase and lowercase differently
                if char.isupper():
                    if shifted_value > ord('Z'):
                        shifted_value -= 26
                    elif shifted_value < ord('A'):
                        shifted_value += 26
                else:
                    if shifted_value > ord('z'):
                        shifted_value -= 26
                    elif shifted_value < ord('a'):
                        shifted_value += 26
                result += chr(shifted_value)
            else:
                # Leave non-alphabetical characters untouched
                result += char

        return result

    def decode(self):
        """Decode the given message using the provided key."""
        result = ''
        for char in self.message:
            if char.isalpha():
                # Reverse the shift by subtracting the key
                shifted_value = ord(char) - self.key
                # Handle uppercase and lowercase differently
                if char.isupper():
                    if shifted_value > ord('Z'):
                        shifted_value -= 26
                    elif shifted_value < ord('A'):
                        shifted_value += 26
                else:
                    if shifted_value > ord('z'):
                        shifted_value -= 26
                    elif shifted_value < ord('a'):
                        shifted_value += 26
                result += chr(shifted_value)
            else:
                # Leave non-alphabetical characters untouched
                result += char
        return result


# Implementation of the Vigenère Cipher algorithm


class VigenereCipher:
    def __init__(self, key: str, handle_non_alpha: bool = True, preserve_case: bool = True, preserve_spacing: bool = True):
        self._validate_input(key)

        self.key = key.lower().replace(' ', '')
        self.handle_non_alpha = handle_non_alpha
        self.preserve_case = preserve_case
        self.preserve_spacing = preserve_spacing

    @staticmethod
    def _validate_input(key: str):
        if not all([c.isalpha() for c in key]) or len(key) < 1:
            raise ValueError(
                "Key must contain only letters and have a length of at least one character")

    def _process_string(self, s: str, mode: int = 0) -> str:
        result = []
        key_length = len(self.key)
        idx = 0

        for symbol in s:
            if symbol.isalpha():
                num = ord(symbol.lower())
                key_num = ord(self.key[idx % key_length]) - ord('a')

                if mode == 0:  # Encryption
                    num = (num - ord('a') + key_num) % 26 + ord('a')
                elif mode == 1:  # Decryption
                    num = (num - ord('a') - key_num) % 26 + ord('a')

                encoded = chr(num)

                if self.preserve_case and symbol.isupper():
                    encoded = encoded.upper()

                result.append(encoded)
                idx += 1
            else:
                if self.preserve_spacing:
                    result.append(symbol)

        result = ''.join(result)
        return result

    def encrypt(self, plaintext: str) -> str:
        return self._process_string(plaintext, mode=0)

    def decrypt(self, ciphertext: str) -> str:
        return self._process_string(ciphertext, mode=1)


class PlayfairCipher:
    def __init__(self, data, key):
        self.data = data
        self.key = key

    @staticmethod
    def prepare_key(key):
        """
        Prepares the key for the Playfair Cipher.
        Removes duplicates, converts the key to uppercase, and handles 'J' as a separate character.
        """
        key = ''.join(set(key.upper()))
        return key

    @staticmethod
    def create_matrix(key):
        """
        Creates the 5x5 Playfair Cipher matrix.
        """
        matrix = []
        remaining_letters = [chr(i)
                             for i in range(65, 91) if chr(i) not in key]
        for char in key + ''.join(remaining_letters):
            if len(matrix) == 0 or len(matrix[-1]) == 5:
                matrix.append([])
            matrix[-1].append(char)
        return matrix

    def encrypt(self):
        plaintext = self.data
        key = self.key
        """
        Encrypts the plaintext using the Playfair Cipher.
        Handles repeated letters in the plaintext by inserting 'X' between them.
        """
        prepared_key = PlayfairCipher.prepare_key(key)
        matrix = PlayfairCipher.create_matrix(prepared_key)
        ciphertext = ""

        plaintext = ''.join(
                    char for char in plaintext.upper() if char.isalpha())
        pairs = []
        for i in range(0, len(plaintext), 2):
            pair = plaintext[i:i+2]
            if len(pair) == 1:
                pair += 'X'
            elif pair[0] == pair[1]:
                pair = pair[0] + 'X' + pair[1]
            pairs.append(pair)
        for pair in pairs:
            row1, col1 = None, None
            row2, col2 = None, None
            for i in range(5):
                for j in range(5):
                    if matrix[i][j] == pair[0]:
                        row1, col1 = i, j
                    elif matrix[i][j] == pair[1]:
                        row2, col2 = i, j
            if row1 == row2:
                ciphertext += matrix[row1][(col1+1) %
                                           5] + matrix[row2][(col2+1) % 5]
            elif col1 == col2:
                ciphertext += matrix[(row1+1) % 5][col1] + \
                    matrix[(row2+1) % 5][col2]
            else:
                ciphertext += matrix[row1][col2] + matrix[row2][col1]
        return ciphertext

    def decrypt(self):
        ciphertext = self.data
        key = self.key
        """
        Decrypts the ciphertext using the Playfair Cipher.
        """
        prepared_key = PlayfairCipher.prepare_key(key)
        matrix = PlayfairCipher.create_matrix(prepared_key)
        plaintext = ""
        ciphertext = ''.join(
            char for char in ciphertext.upper() if char.isalpha())
        pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        for pair in pairs:
            row1, col1 = None, None
            row2, col2 = None, None
            for i in range(5):
                for j in range(5):
                    if matrix[i][j] == pair[0]:
                        row1, col1 = i, j
                    elif matrix[i][j] == pair[1]:
                        row2, col2 = i, j
            if row1 == row2:
                plaintext += matrix[row1][(col1-1) %
                                          5] + matrix[row2][(col2-1) % 5]
            elif col1 == col2:
                plaintext += matrix[(row1-1) % 5][col1] + \
                    matrix[(row2-1) % 5][col2]
            else:
                plaintext += matrix[row1][col2] + matrix[row2][col1]
            # Replace placeholder X with originall value
            f_result = ""
            for i in range(len(plaintext)):
                if i == 0 or plaintext[i] != 'X':
                    f_result += plaintext[i]
                else:
                    f_result += plaintext[i-1]
        return f_result.lower()


def write2file(dt, fname):
    logger.info(f"Writing to \033[1;92m{fname}\033[0m")
    try:
        with open(fname, 'w') as f:
            f.write(dt)
            logger.info("\033[92mOk\033[0m")
    except FileExistsError:
        print("\033[1;92mFound existing file with similar name \033[0m")
        sys.exit(1)


def readfile(fname):
    logger.info(f"Read \033[1;92m{fname}\033[0m")
    try:
        with open(fname, 'r') as f:
            data = f.read()
            logger.info("\033[92mOk\033[0m")
            # print(data)
    except FileExistsError:
        print("\033[1;92mFile Not Found\033[0m")
        sys.exit(1)
    return data


def enc_control(file, cipher, key=None):
    print("\033[1;32mComencing encryption process\033[0m")
    fname = file + '.enc'

    if cipher.lower() == "caesar" or cipher.lower() == "caesarcipher":
        try:
            if os.path.isfile(file):
                data = readfile(file)
                logger.info("Call Caesar...")
                init = CaesarCipher(data)
                dt = init.encode()
                print(dt)
                write2file(dt, fname)

            elif os.path.isdir(file):
                file_list = ubundledir(file)
                for file in file_list:
                    data = readfile(file)
                    init = CaesarCipher(data)
                    dt = init.encode()
                    write2file(dt, fname)
                logger.info("\033[1;92mDone")
            else:
                init = CaesarCipher(file)
                init.caesar_enc_cipher()

        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.debug(e)

    elif cipher.lower() == "playfaircipher" or cipher.lower() == "playfair":
        if key:
            key = "MCIPHERS"
        try:
            if os.path.isfile(file):
                data = readfile(file)
                init = PlayfairCipher(data, key)
                dt = init.encrypt()
                write2file(dt, fname)
            elif os.path.isdir(file):
                file_list = ubundledir(file)
                for file in file_list:
                    data = readfile(file)
                    init = VigenereCipher(data)
                    init.encrypt()
                    write2file(dt, fname)
                logger.info("\033[1;92mDone")
            else:
                init = PlayfairCipher(file, key)
                init.encrypt()

        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.debug(e)

    elif cipher.lower() == "vigenere" or cipher.lower() == "vigenerecipher":

        try:
            vc = VigenereCipher(
                key="PYTHON", handle_non_alpha=True, preserve_case=True, preserve_spacing=True)

            if os.path.isfile(file):
                data = readfile(file)
                ct = vc.encrypt(data)
                write2file(ct, fname)
            elif os.path.isdir(file):
                file_list = ubundledir(file)
                for file in file_list:
                    data = readfile(file)
                    ct = vc.encrypt(data)
                    write2file(ct, fname)
                logger.info("\033[1;92mDone")
            else:
                ct = vc.encrypt(file, key)

        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.debug(e)


def dec_control(file, cipher, key=None):
    fname = file[:-4]
    print("\033[1;32mComencing deryption process\033[0m")
    if cipher.lower() == "caesar" or cipher.lower() == "caesarcipher":
        try:
            if os.path.isfile(file):
                data = readfile(file)
                init = CaesarCipher(data)
                dt = init.decode()
                write2file(dt, fname)

            elif os.path.isdir(file):
                file_list = ubundledir(file)
                for file in file_list:
                    data = readfile(file)
                    init = CaesarCipher(data)
                    dt = init.decode()
                    write2file(dt, fname)
                logger.info("\033[1;92mDone")
            else:
                init = CaesarCipher(file)
                init.decode()
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.debug(e)

    elif cipher.lower() == "playfaircipher" or cipher.lower() == "playfair":
        try:
            if os.path.isfile(file):
                data = readfile(file)
                init = PlayfairCipher(data, key)
                dt = init.decrypt()
                write2file(dt, file)
            elif os.path.isdir(file):
                file_list = ubundledir(file)
                for file in file_list:
                    data = readfile(file)
                    init = VigenereCipher(data)
                    init.decrypt()
                    write2file(dt, fname)
                logger.info("\033[1;92mDone")
            else:
                init = PlayfairCipher(file, key)
                init.encrypt()
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.debug(e)

    elif cipher.lower() == "vigenere" or cipher.lower() == "vigenerecipher":
        try:
            vc = VigenereCipher(
                key="PYTHON", handle_non_alpha=True, preserve_case=True, preserve_spacing=True)

            if os.path.isfile(file):
                data = readfile(file)
                ct = vc.decrypt(data)
                write2file(ct, fname)
            elif os.path.isdir(file):
                file_list = ubundledir(file)
                for file in file_list:
                    data = readfile(file)
                    ct = vc.decrypt(data)
                    write2file(ct, fname)
                logger.info("\033[1;92mDone")
            else:
                ct = vc.encrypt(file)
        except KeyboardInterrupt:
            print("\nExiting")
            sys.exit(1)
        except Exception as e:
            logger.debug(e)


def ubundledir(par_dir):
    ls = []
    try:
        # Iterate over all files in the folder
        for root, dirs, files in os.walk(par_dir):
            sz = len(files)
            for file in files:

                file_path = os.path.join(root, file)
                ls.append(file_path)

        print(f"\033[1;93mFound:\033[1;95m{sz}")

        return ls
    except KeyboardInterrupt:
        print("\nExiting")
        sys.exit(1)
    except Exception as e:
        print(f"\033[31m{e}\033[0m")


if __name__ == "__main__":
    dec_control("test.txt.enc", "vigenere")
    ''' CaesarCipher
    with open("dd.py", 'r') as f:
        ms = f.read()
    init = CaesarCipher(ms)
    encoded_msg = init.encode()
    print("Encode message:: ", encoded_msg)
    init = CaesarCipher(encoded_msg)
    decoded_msg = init.decode()
    print("decoded message:: ", decoded_msg)

    # PlayfairCipher
    key = "PLAYFAIREXAMPLE"
    with open("dd.py", 'r') as f:
        ms = f.read()
    # plaintext = "Hello, World!"
    cipher = PlayfairCipher(ms, key)
    ciphertext = cipher.encrypt()
    print("\nPlaintext:", ms)
    print("\nCiphertext:", ciphertext)
    cipher = PlayfairCipher(ciphertext, key)
    plaintext = cipher.decrypt()
    print("\nDecrypted data:", plaintext)

    VigenereCipher
    with open("dd.py", 'r') as f:
        ms = f.read()
    vc = VigenereCipher(
        key="PYTHON", handle_non_alpha=True, preserve_case=True, preserve_spacing=True)
    pt = "This is some sample 342 text."
    ct = vc.encrypt(ms)
    dt = vc.decrypt(ct)
    print(
        f"Original Text:\n{pt}\n\nEncoded Text:\n{ct}\n\nDecoded Text:\n{dt}")'''
