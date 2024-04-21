import argparse
import os

from . import fedbanner
from .enc_dec import decrypt_file, decrypt_folder, encrypt_file, encrypt_folder
from . master_ED import HandleFiles, HandleFolders
from .mciphers import dec_control, enc_control


def main():
    # create argument parser
    parser = argparse.ArgumentParser(
        description='''Encrypt or decrypt files and folders''')
    # Define required arguments
    parser.add_argument(
        '-m', '--mode', choices=["encrypt", "decrypt"], help="\
Mode:encryption or decryption", required=True)
    parser.add_argument('-i', '--input_file', type=str,
                        help='Input file path or folder', required=True)

    parser.add_argument('-Rk', '--random_key', type=str,
                        help='decryption key to be used')
    parser.add_argument('-p', '--passphrase', type=str,
                        help='Encryption/decryption passphrase/password to \
be used')
    parser.add_argument(
        "-c", "--cipher", help="cipher to be used, avaiable ciphers:\
        [\033[1;34mcaesar, PlayfairCipher, vigenere\033[0m]")

    # Parse the commandline arguments
    args = parser.parse_args()
    input_file = args.input_file

    # Handle file/folder encryption
    if args.mode == 'encrypt':

        # Handle cipher choices
        if args.cipher:
            # Since caesar cipher needs no passphrase, ommit it
            if args.cipher.lower() == 'caesar':
                args.passphrase = None
                args.random_key = None
            enc_control(args. input_file, args.cipher, args.passphrase)

        # Handle if passphrase is provided
        if os.path.isfile(input_file) and args.passphrase:
            init = HandleFiles(args.input_file, args.passphrase)
            init.encrypt_file()

        elif os.path.isdir(input_file) and args.passphrase:
            init = HandleFolders(args.input_file, args.passphrase)
            init.encrypt_folder()

        # Handle case where encryption passphrase is not provided
        elif os.path.isfile(input_file) and args.random_key:
            encrypt_file(input_file)

        # Handle case where passphrase is not provided but random key is provided
        elif os.path.isdir(input_file) and args.random_key:
            encrypt_folder(input_file)

        # Handle case where neither passphrase is provided nor -Rk flag is passed
        elif not args.random_key and not args.passphrase and not args.cipher:
            print("An encryption passphrase is needed otherwise try the command again with '--Rk' flag to use a randomly generated encryption key")

    # Handle file/folder decryption
    if args.mode == 'decrypt':

        # Handle cipher choices
        if args.cipher:
            # Since caesar cipher needs no passphrase, ommit it
            if args.cipher.lower() == 'caesar' or args.cipher.lower() == 'caesarcipher':
                args.passphrase = None
                args.random_key = None
            dec_control(args. input_file, args.cipher, args.passphrase)

        # Handle if passphrase is provided
        if os.path.isfile(input_file) and args.passphrase:
            init = HandleFiles(args. input_file, args.passphrase)
            init.decrypt_file()

        elif os.path.isdir(input_file) and args.passphrase:
            init = HandleFolders(args.input_file, args.passphrase)
            init.decrypt_folder()

        # Handle case where decryption passphrase is not provided
        elif os.path.isfile(input_file) and args.random_key:
            decrypt_file(input_file, args.random_key)

        elif os.path.isdir(input_file) and args.random_key:
            decrypt_folder(input_file, args.random_key)

        # Handle case where neither passphrase is provided nor -Rk flag is passed
        elif not args.random_key and not args.passphrase and not args.cipher:
            print("A decryption passphrase is needed otherwise pass command with '--Rk' or '--cipher' flag to search for encryption key in default key file")


if __name__ == "__main__":
    fedbanner
    main()
