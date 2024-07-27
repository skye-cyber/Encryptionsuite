import argparse
import logging
import logging.handlers
import os
import sys
from .banner import _banner_
# from getpass import getpass
from .enc_dec import decrypt_file, decrypt_folder, encrypt_file, encrypt_folder
from .master_ED import HandleFiles, HandleFolders
from .ciphers import dec_control, enc_control
from .mores_cipher import _dec_control_, _enc_control_

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


def clean_Encfile(input_file):
    _orig_ = input_file
    for i in range(int(input_file[-1:]), -1, -1):
        file = f'{input_file[:-1]}{i}'
        while os.path.exists(file) and file != f'{input_file[:-1]}{_orig_[-1:]}':
            print(f"\033[2;35mDelete \033[1m{file}🚮\033[0m")
            os.remove(file)
            break


def _clean_Origfile_(input_file):
    _orig_ = input_file
    for i in range(int(input_file[-1:])):
        file = f'{input_file[:-1]}{i}'
        while os.path.exists(file) and file != f'{input_file[-1:]}{_orig_[-1:]}':
            print(f"\033[2;35mDelete \033[1m{file}🚮\033[0m")
            os.remove(file)
            break


def _clean_dir_(gdir, mode):
    try:
        # Delete all original files
        for root, dirs, files in os.walk(gdir):
            for file in files:
                _path_ = os.path.join(root, file)

                # Clean enc files
                if mode is True:

                    if _path_[:-1].endswith('enc') and os.path.exists(_path_[:-5]):
                        print(f"\033[2;35mDelete \033[1m{_path_}🚮\033[0m")
                        os.remove(_path_)

                # Clean original files
                if mode is False:

                    if not _path_[:-1].endswith('enc') and (os.path.exists(_path_ + f'.enc{0}') or os.path.exists(_path_ + f'.enc{1}')):
                        print(f"\033[2;35mDelete \033[1m{_path_}🚮\033[0m")
                        os.remove(_path_)

                    if _path_[:-1].endswith('enc') and os.path.exists(_path_ + f'.enc{0}') and os.path.exists(_path_ + f'.enc{1}'):
                        os.remove(_path_ + f'.enc{0}')

    except Exception as e:
        print(f"\033[31m{e}\033[0m")
    # finally:
    # print("\033[92mSucceed✅\033[0m")


def get_keys(pf):
    with open(pf) as f:
        ps = f.read()
    return ps.split(',')


def main():
    # create argument parser
    Note = "\033[96mPassword option does not work for caesar_cipher and mores_cipher\033[0m"
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt files and folders", epilog=Note)
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
be used\033[1;94m Password(will be hidden)\033[0m')
    parser.add_argument(
        "-c", "--cipher", help="cipher to be used, avaiable ciphers:\
        [\033[1;34mcaesar, PlayfairCipher, vigenere, mores_cipher\033[0m]")

    parser.add_argument("--pass_list", "-pl", help=f"""Provide passwords list or file containing \
password list for decryptiona and encryption""")
    # Print banner alongside help message
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        _banner_()

        # Parse the commandline arguments
    args = parser.parse_args()
    input_file = args.input_file
    passphrase = args.passphrase
    cipher = args.cipher

    _caesar_ = {"caesar", "caesar_cipher", "caesarcipher"}
    _more_ = {"mores", "mores_cipher", "morescipher", "mores-cipher"}

    _secure_ = False
    # If no cipher nor passphrase is provide orcipher not the cipher set, request for passphrase
    '''if not passphrase and (cipher not in (_caesar_ or _more_) or not cipher):
        try:
            passphrase = getpass("Enter password: ")
            print(f"Password length: {len(passphrase)}")
            _secure_ = True
        except KeyboardInterrupt:
            print("\nQuit❕")
            sys.exit(1)
        except Exception as e:
            print(f"\033[91m{e}\033[0m")
            sys.exit(2)'''

    if not os.path.exists(input_file):
        print("\033[1mFile does not exist\033[0m")
        sys.exit(0)
    # Handle file/folder encryption
    if args.mode == 'encrypt':
        logger.info("\033[1;32m======START@Deryption======\033[0m")
        # Handle cipher choices
        if args.cipher:
            # mores_cypher does not require password
            if args.cipher.lower() in set(_more_):
                _enc_control_(input_file)

            # Since caesar cipher needs no passphrase, ommit it
            if args.cipher.lower() in set(_caesar_):
                if args.pass_list:
                    print(
                        "\033[91mSorry caesar and mores cipher accept not password list\033[0m")
                    prompt = input("Press enter to continue")
                    if prompt.lower() == 'c':
                        sys.exit()
                    else:
                        pass

                args.passphrase = None
                args.random_key = None
                enc_control(input_file, cipher, passphrase)

            if args.pass_list:
                pass_ls = get_keys(args.pass_list) if os.path.exists(
                    args.pass_list) else list(args.pass_list)
                e_level = 0

                for pass_key in pass_ls:
                    enc_control(input_file,
                                args.cipher, pass_key)
                    input_file = f'{input_file}'f'.enc{e_level}' if input_file[-4:-
                                                                               1] != "enc" else f'{input_file[:-1]}'f'{e_level}'
                    e_level += 1

                # Clean intermediary files
                _clean_Origfile_(input_file)

            elif args.passphrase:
                logger.info(
                    f"\033[1m@key=\033[30m{passphrase}\033[0m")
                enc_control(input_file, args.cipher, args.passphrase)

        # Handle if passphrase or a password list file is provided
        if os.path.isfile(input_file) and (args.passphrase or args.pass_list):
            if args.pass_list:
                pass_ls = get_keys(args.pass_list) if os.path.exists(
                    args.pass_list) else list(args.pass_list)
                e_level = 0

                for pass_key in pass_ls:
                    init = HandleFiles(input_file, pass_key)
                    init.encrypt_file()
                    input_file = f'{input_file}'f'.enc{e_level}' if input_file[-4:-
                                                                               1] != "enc" else f'{input_file[:-1]}'f'{e_level}'
                    e_level += 1

                # Clean intermediary files
                _clean_Origfile_(input_file)

            elif args.passphrase:
                init = HandleFiles(args.input_file, args.passphrase)
                init.encrypt_file()

        elif os.path.isdir(input_file) and (args.passphrase or args.pass_list):
            try:
                if args.pass_list:
                    pass_ls = get_keys(args.pass_list) if os.path.exists(
                        args.pass_list) else list(args.pass_list)
                    e_level = 0

                    for pass_key in pass_ls:
                        init = HandleFolders(input_file, pass_key)
                        init.encrypt_folder()
                        input_file = f'{input_file}'f'.enc{e_level}' if input_file[-4:-
                                                                                   1] != "enc" else f'{input_file[:-1]}'f'{e_level}'
                        e_level += 1

                    # Clean intermediary files
                    _clean_Origfile_(input_file)

                elif args.passphrase:
                    logger.info(
                        f"\033[1m@key lenth=\033[30m{len(passphrase)}\033[0m")
                    init = HandleFolders(input_file, args.passphrase)
                    init.encrypt_folder()

            finally:
                # Clean original files from the directory
                # print("\033[33mClean\033[0m")
                _clean_dir_(input_file, False)

        # Handle case where encryption passphrase is not provided
        elif os.path.isfile(input_file) and args.random_key:
            encrypt_file(input_file)

        # Handle case where passphrase is not provided but random key is provided
        elif os.path.isdir(input_file) and args.random_key:
            encrypt_folder(input_file)

        # Handle case where neither passphrase is provided nor -Rk flag is passed
        elif not args.random_key and not args.passphrase and not args.cipher and not args.pass_list and _secure_ is not True:
            print("An encryption passphrase is needed otherwise try the command again with '--Rk' flag to use a randomly generated encryption key")
        logger.info("\033[1;92mDone")

    # Handle file/folder decryption
    if args.mode == 'decrypt':
        if os.path.isfile(input_file) and input_file[-4:-1] != "enc":
            print("\033[1mThe file doesn not appear to be encrypted\033[0m")
            sys.exit(0)

        logger.info("\033[1;32m======START@Deryption======\033[0m")

        # Handle cipher choices
        if args.cipher:

            if args.cipher.lower() in list(_more_):
                _dec_control_(input_file)

            # Since caesar cipher needs no passphrase, ommit it
            elif args.cipher.lower() in list(_caesar_):

                # Caesar cipher accepts no pass list so prompt to continue without it
                if args.pass_list:
                    print(
                        "\033[91mOops☠️ caesar cipher accepts no password list\033[0m")
                    prompt = input("Press enter to continue")
                    if prompt.lower() == 'c':
                        sys.exit()
                    else:
                        pass

                passphrase = None
                args.random_key = None
                logger.info(f"\033[1m@key=\033[30m{passphrase}\033[0m")
                dec_control(input_file, cipher, passphrase)
            elif args.pass_list:
                pass_ls = get_keys(args.pass_list) if os.path.exists(
                    args.pass_list) else list(args.pass_list)
                e_level = int(input_file[-1:])
                print(
                    f"\033[1;93mLevel \033[92m{e_level}\033[1;93m encryption detected\033[0m")

                if e_level + 1 != len(pass_ls):
                    print(
                        "\033[31mPassword mismatch for the used encryption level\033[0m")
                    sys.exit(1)

                for pass_key in reversed(pass_ls):
                    logger.info(
                        f"\033[1m@key=\033[30m{pass_key}\033[0m")
                    dec_control(input_file,
                                args.cipher, pass_key)
                    input_file = f'{input_file[:-1]}'f'{e_level - 1}'

                # Clean intermediary files
                clean_Encfile(input_file)

            elif passphrase:
                logger.info(
                    f"\033[1m@key=\033[30m{passphrase}\033[0m")
                dec_control(input_file, args.cipher, args.passphrase)

        # Handle case where no cipher is selcted and passphrase/password is provided
        if os.path.isfile(input_file) and (args.passphrase or args.pass_list):

            if args.pass_list:
                pass_ls = get_keys(args.pass_list) if os.path.exists(
                    args.pass_list) else list(args.pass_list)
                e_level = int(input_file[-1:])
                print(
                    f"\033[1;93mLevel \033[92m{e_level + 1}\033[1;93m encryption detected\033[0m")

                if e_level + 1 != len(pass_ls):
                    print(
                        "\033[31mPassword mismath for the used encryption level\033[0m")
                    sys.exit(1)

                for pass_key in reversed(pass_ls):
                    logger.info(
                        f"\033[1m@key=\033[30m{pass_key}\033[0m")
                    init = HandleFiles(input_file, pass_key)
                    init.decrypt_file()
                    input_file = f'{input_file[:-1]}'f'{e_level - 1}'

                # Clean intermediary files
                clean_Encfile(input_file)

            elif args.passphrase:
                logger.info(
                    f"\033[1m@key=\033[30m{passphrase}\033[0m")
                init = HandleFiles(input_file, args.passphrase)
                init.decrypt_file()

        elif os.path.isdir(input_file) and args.passphrase:

            if input_file[-4:-1] != 'enc':
                pass
            try:
                if args.pass_list:
                    pass_ls = get_keys(args.pass_list) if os.path.exists(
                        args.pass_list) else list(args.pass_list)
                    e_level = int(input_file[-1:])
                    print(
                        f"\033[1;93mLevel \033[92m{e_level}\033[1;93m encryption detected\033[0m")
                    if e_level + 1 != len(pass_ls):
                        print("Password mismath for the used encryption level")
                        sys.exit(1)

                    for pass_key in reversed(pass_ls):
                        logger.info(
                            f"\033[1m@key=\033[30m{pass_key}\033[0m")
                        init = HandleFolders(input_file, pass_key)
                        init.decrypt_folder()
                        input_file = f'{input_file[:-1]}'f'{e_level - 1}'

                    # Clean intermediary files
                    clean_Encfile(input_file)

                elif args.passphrase:
                    logger.info(
                        f"\033[1m@key=\033[30m{passphrase}\033[0m")
                    init = HandleFolders(input_file, args.passphrase)
                    init.decrypt_folder()

            finally:
                # Clean original enc files from the directory
                # print("\033[33mClean\033[0m")
                _clean_dir_(input_file, True)

        # Handle case where decryption passphrase is not provided
        elif os.path.isfile(input_file) and args.random_key:
            decrypt_file(input_file, args.random_key)

        elif os.path.isdir(input_file) and args.random_key:
            decrypt_folder(input_file, args.random_key)

        # Handle case where neither passphrase is provided nor -Rk flag is passed
        elif not args.random_key and not args.passphrase and not args.cipher:
            print("A decryption passphrase is needed otherwise pass command with '--Rk' or '--cipher' flag to search for encryption key in default key file")

        logger.info("\033[1;92m======END======")


if __name__ == "__main__":
    main()
