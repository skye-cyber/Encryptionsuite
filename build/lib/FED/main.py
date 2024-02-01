import os
import argparse
from .enc_dec import encrypt_file
from .enc_dec import decrypt_file
from .enc_dec import encrypt_folder
from .enc_dec import decrypt_folder


def main():
    # create argument parser
    parser = argparse.ArgumentParser(description='''Encrypt or decrypt files and folders''')
    # Define required arguments
    parser.add_argument('-m', '--mode', choices=["encrypt", "decrypt"], help="Mode:encryption or decryption", required=True)
    parser.add_argument('-i', '--input_file', type=str, help='Input file path or folder', required=True)
    # parser.add_argument('-o', '--output_file', type=str, help='Output file', required=True)
    parser.add_argument('-k', '--key', type=str, help='decryption key to be used')

    # Parse the commandline arguments
    args = parser.parse_args()
    input_file = args.input_file
    # output_file = args.output_file
    decryption_key = args.key

    # Call the imported script and parse the input and output files
    # subprocess.call['python', 'enc_dec.py', input_file, output_file, decryption_key]

    # Corrected if conditions
    if args.mode == 'encrypt':
        if os.path.isfile(input_file):
            encrypt_file(input_file)
        elif os.path.isdir(input_file):
            encrypt_folder(input_file)
    if args.mode == 'decrypt':
        if os.path.isfile(input_file):
            decrypt_file(input_file, decryption_key)
        elif os.path.isdir(input_file):
            decrypt_folder(input_file, decryption_key)


if __name__ == "__main__":
    main()
