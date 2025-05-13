import argparse
import logging
import logging.handlers
import os
import sys
from rich.logging import RichHandler
from .banner import _banner_
from .bruteforce import Bruteforce
from .ciphers import dec_control, enc_control
from .colors import (
    BWHITE,
    CGREEN,
    BLUE,
    CYAN,
    DGREEN,
    DYELLOW,
    FCYAN,
    FMAGENTA,
    GREEN,
    RED,
    RESET,
)
from .enc_dec import decrypt_file, decrypt_folder, encrypt_file, encrypt_folder
from .master_ED import HandleFiles, HandleFolders
from .mores_cipher import _dec_control_, _enc_control_

logging.basicConfig(
    level=logging.INFO,
    format="- [%(levelname)s] - %(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)


def clean_Encfile(input_file):
    _orig_ = input_file
    for i in range(int(input_file[-1:]), -1, -1):
        file = f"{input_file[:-1]}{i}"
        while os.path.exists(file) and file != f"{input_file[:-1]}{_orig_[-1:]}":
            print(f"{FMAGENTA}Delete {BWHITE}{file}🚮{RESET}")
            os.remove(file)
            break


def _clean_Origfile_(input_file):
    _orig_ = input_file
    for i in range(int(input_file[-1:])):
        file = f"{input_file[:-1]}{i}"
        while os.path.exists(file) and file != f"{input_file[-1:]}{_orig_[-1:]}":
            print(f"{FMAGENTA}Delete {BWHITE}{file}🚮{RESET}")
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
                    if _path_[:-1].endswith("enc") and os.path.exists(_path_[:-5]):
                        print(f"{FMAGENTA}Delete {BWHITE}{_path_}🚮{RESET}")
                        os.remove(_path_)

                # Clean original files
                if mode is False:
                    if not _path_[:-1].endswith("enc") and (
                        os.path.exists(_path_ + f".enc{0}")
                        or os.path.exists(_path_ + f".enc{1}")
                    ):
                        print(f"{FMAGENTA}Delete {BWHITE}{_path_}🚮{RESET}")
                        os.remove(_path_)

                    if (
                        _path_[:-1].endswith("enc")
                        and os.path.exists(_path_ + f".enc{0}")
                        and os.path.exists(_path_ + f".enc{1}")
                    ):
                        os.remove(_path_ + f".enc{0}")

    except Exception as e:
        print(f"{RED}{e}{RESET}")


def ArgsMain():
    # create argument parser
    Note = f"{CYAN}Password option does not work for caesar_cipher and mores_cipher.{RESET}"
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt files and folders",
        epilog=Note + "\n",
        add_help=False,
    )
    # Define required arguments
    parser.add_argument(
        "-enc",
        "--encrypt",
        action="store_true",
        help="Encrypt file/folder",
    )

    parser.add_argument(
        "-dec",
        "--decrypt",
        action="store_true",
        help="Decrypt file/folder",
    )

    parser.add_argument(
        "-i", "--input_file", type=str, help="Input file path or folder"
    )

    parser.add_argument(
        "-Rk", "--random_key", type=str, help="decryption key to be used"
    )
    parser.add_argument(
        "-p",
        "--passphrase",
        type=str,
        help="Encryption/decryption passphrase/password to be used",
    )  # {DBLUE} Password(will be hidden){RESET}')
    parser.add_argument(
        "-c",
        "--cipher",
        help=f"cipher to be used, avaiable ciphers:\
        [\033[1;34mcaesar, PlayfairCipher, vigenere, mores_cipher{RESET}]",
    )

    parser.add_argument(
        "--pass_list",
        "-pl",
        help="""Provide passwords list or file containing password list for decryptiona and encryption""",
    )
    parser.add_argument(
        "-b",
        "--bruteforce",
        help="Run a list of words/passphrases against the file/folder to see which works.",
    )
    parser.add_argument(
        "-h", "--help", action="store_true", help="Show this help message and exit"
    )

    # Parse the commandline arguments
    init = argsOPMaper(parser)
    init.run()


"""    input_file = args.input_file
    passphrase = args.passphrase
    cipher = args.cipher

    _caesar_ = {"caesar", "caesar_cipher", "caesarcipher"}
    _more_ = {"mores", "mores_cipher", "morescipher", "mores-cipher"}
    _playfair_ = {"playfaircipher", "playfair"}

    _secure_ = False

    if not os.path.exists(input_file):
        print(f"{BWHITE}File does not exist{RESET}")
        sys.exit(0)

    # Handle file/folder encryption
    if args.encrypt:
        logger.info(f"{DGREEN}======START@Encryption======{RESET}")
        # Handle cipher choices
        if args.cipher:
            # check whether the cipher is prsent
            if args.cipher not in (_caesar_.union(_more_, _playfair_)):
                logger.setLevel("CRITICAL")
                logger.critical(f"\033[95m{args.cipher}\033[0m cipher not found")
                exit(2)
            # mores_cypher does not require password
            if not args.passphrase and args.cipher.lower() in _playfair_:
                logger.error("Please provide passphrase")
                exit(1)

            if args.cipher.lower() in set(_more_):
                _enc_control_(input_file)
                exit(0)

            # Since caesar cipher needs no passphrase, ommit it
            if args.cipher.lower() in set(_caesar_):
                if args.pass_list:
                    print(
                        f"{RED}Sorry caesar and mores cipher accept not password list{RESET}"
                    )
                    prompt = input("Press enter to continue")
                    if prompt.lower() == "c":
                        sys.exit()
                    else:
                        pass

                args.passphrase = None
                args.random_key = None
                enc_control(input_file, cipher, passphrase)

            if args.pass_list:
                pass_ls = (
                    get_keys(args.pass_list)
                    if os.path.exists(args.pass_list)
                    else list(args.pass_list)
                )
                e_level = 0

                for pass_key in pass_ls:
                    enc_control(input_file, args.cipher, pass_key)
                    input_file = (
                        f"{input_file}" f".enc{e_level}"
                        if input_file[-4:-1] != "enc"
                        else f"{input_file[:-1]}" f"{e_level}"
                    )
                    e_level += 1

                # Clean intermediary files
                _clean_Origfile_(input_file)

            elif args.passphrase:
                logger.info(f"{BWHITE}@key={CGREEN}{passphrase}{RESET}")
                enc_control(input_file, args.cipher, args.passphrase)

        # Handle if passphrase or a password list file is provided
        if os.path.isfile(input_file) and (args.passphrase or args.pass_list):
            if args.pass_list:
                pass_ls = (
                    get_keys(args.pass_list)
                    if os.path.exists(args.pass_list)
                    else list(args.pass_list)
                )
                e_level = 0

                for pass_key in pass_ls:
                    init = HandleFiles(input_file, pass_key)
                    init.encrypt_file()
                    input_file = (
                        f"{input_file}" f".enc{e_level}"
                        if input_file[-4:-1] != "enc"
                        else f"{input_file[:-1]}" f"{e_level}"
                    )
                    e_level += 1

                # Clean intermediary files
                _clean_Origfile_(input_file)

            elif args.passphrase:
                init = HandleFiles(args.input_file, args.passphrase)
                init.encrypt_file()

        elif os.path.isdir(input_file) and (args.passphrase or args.pass_list):
            try:
                if args.pass_list:
                    pass_ls = (
                        get_keys(args.pass_list)
                        if os.path.exists(args.pass_list)
                        else list(args.pass_list)
                    )
                    e_level = 0

                    for pass_key in pass_ls:
                        init = HandleFolders(input_file, pass_key)
                        init.encrypt_folder()
                        input_file = (
                            f"{input_file}" f".enc{e_level}"
                            if input_file[-4:-1] != "enc"
                            else f"{input_file[:-1]}" f"{e_level}"
                        )
                        e_level += 1

                    # Clean intermediary files
                    _clean_Origfile_(input_file)

                elif args.passphrase:
                    logger.info(f"{BWHITE}@key lenth={CGREEN}{len(passphrase)}{RESET}")
                    init = HandleFolders(input_file, args.passphrase)
                    init.encrypt_folder()

            finally:
                # Clean original files from the directory
                # print("\033[33mClean{RESET}")
                _clean_dir_(input_file, False)

        # Handle case where encryption passphrase is not provided
        elif os.path.isfile(input_file) and args.random_key:
            encrypt_file(input_file)

        # Handle case where passphrase is not provided but random key is provided
        elif os.path.isdir(input_file) and args.random_key:
            encrypt_folder(input_file)

        # Handle case where neither passphrase is provided nor -Rk flag is passed
        elif (
            not args.random_key
            and not args.passphrase
            and not args.cipher
            and not args.pass_list
            and _secure_ is not True
        ):
            print(
                "An encryption passphrase is needed otherwise try the command again with '--Rk' flag to use a randomly generated encryption key"
            )
        logger.info(f"{DGREEN}Done")

    # Handle file/folder decryption
    if args.decrypt:
        if os.path.isfile(input_file) and input_file[-4:-1] != "enc":
            print(f"{BWHITE}The file doesn not appear to be encrypted{RESET}")
            sys.exit(0)

        logger.info(f"{DGREEN}======START@Deryption======{RESET}")

        if args.bruteforce:
            init = Bruteforce(input_file, args.bruteforce)
            init.conservative()
        # Handle cipher choices
        if args.cipher:
            if args.cipher.lower() in list(_more_):
                _dec_control_(input_file)

            # Since caesar cipher needs no passphrase, ommit it
            elif args.cipher.lower() in list(_caesar_):
                # Caesar cipher accepts no pass list so prompt to continue without it
                if args.pass_list:
                    print(f"{RED}Oops☠️ caesar cipher accepts no password list{RESET}")
                    prompt = input("Press enter to continue")
                    if prompt.lower() == "c":
                        sys.exit()
                    else:
                        pass

                passphrase = None
                args.random_key = None
                logger.info(f"{BWHITE}@key={CGREEN}{passphrase}{RESET}")
                dec_control(input_file, cipher, passphrase)
            elif args.pass_list:
                pass_ls = (
                    get_keys(args.pass_list)
                    if os.path.exists(args.pass_list)
                    else list(args.pass_list)
                )
                e_level = int(input_file[-1:])
                print(
                    f"{DYELLOW}Level {GREEN}{e_level}{DYELLOW} encryption detected{RESET}"
                )

                if e_level + 1 != len(pass_ls):
                    print(
                        f"{RED}Password mismatch for the used encryption level{RESET}"
                    )
                    sys.exit(1)

                for pass_key in reversed(pass_ls):
                    logger.info(f"{BWHITE}@key={CGREEN}{pass_key}{RESET}")
                    dec_control(input_file, args.cipher, pass_key)
                    input_file = f"{input_file[:-1]}" f"{e_level - 1}"

                # Clean intermediary files
                clean_Encfile(input_file)

            elif passphrase:
                logger.info(f"{BWHITE}@key={CGREEN}{passphrase}{RESET}")
                dec_control(input_file, args.cipher, args.passphrase)

        # Handle case where no cipher is selcted and passphrase/password is provided
        if os.path.isfile(input_file) and (args.passphrase or args.pass_list):
            if args.pass_list:
                pass_ls = (
                    get_keys(args.pass_list)
                    if os.path.exists(args.pass_list)
                    else list(args.pass_list)
                )
                e_level = int(input_file[-1:])
                print(
                    f"{DYELLOW}Level {GREEN}{e_level + 1}{DYELLOW} encryption detected{RESET}"
                )

                if e_level + 1 != len(pass_ls):
                    print(f"{RED}Password mismath for the used encryption level{RESET}")
                    sys.exit(1)

                for pass_key in reversed(pass_ls):
                    logger.info(f"{BWHITE}@key={CGREEN}{pass_key}{RESET}")
                    init = HandleFiles(input_file, pass_key)
                    init.decrypt_file()
                    input_file = f"{input_file[:-1]}" f"{e_level - 1}"

                # Clean intermediary files
                clean_Encfile(input_file)

            elif args.passphrase:
                logger.info(f"{BWHITE}@key={CGREEN}{passphrase}{RESET}")
                init = HandleFiles(input_file, args.passphrase)
                init.decrypt_file()

        elif os.path.isdir(input_file) and args.passphrase:
            if input_file[-4:-1] != "enc":
                pass
            try:
                if args.pass_list:
                    pass_ls = (
                        get_keys(args.pass_list)
                        if os.path.exists(args.pass_list)
                        else list(args.pass_list)
                    )
                    e_level = int(input_file[-1:])
                    print(
                        f"{DYELLOW}Level {GREEN}{e_level}{DYELLOW} encryption detected{RESET}"
                    )
                    if e_level + 1 != len(pass_ls):
                        print("Password mismath for the used encryption level")
                        sys.exit(1)

                    for pass_key in reversed(pass_ls):
                        logger.info(f"{BWHITE}@key={CGREEN}{pass_key}{RESET}")
                        init = HandleFolders(input_file, pass_key)
                        init.decrypt_folder()
                        input_file = f"{input_file[:-1]}" f"{e_level - 1}"

                    # Clean intermediary files
                    clean_Encfile(input_file)

                elif args.passphrase:
                    logger.info(f"{BWHITE}@key={CGREEN}{passphrase}{RESET}")
                    init = HandleFolders(input_file, args.passphrase)
                    init.decrypt_folder()

            finally:
                # Clean original enc files from the directory
                # print("\033[33mClean{RESET}")
                _clean_dir_(input_file, True)

        # Handle case where decryption passphrase is not provided
        elif os.path.isfile(input_file) and args.random_key:
            decrypt_file(input_file, args.random_key)

        elif os.path.isdir(input_file) and args.random_key:
            decrypt_folder(input_file, args.random_key)

        # Handle case where neither passphrase is provided nor -Rk flag is passed
        elif not args.random_key and not args.passphrase and not args.cipher:
            print(
                "A decryption passphrase is needed otherwise pass command with '--Rk' or '--cipher' flag to search for encryption key in default key file"
            )

        logger.info(f"{DGREEN}====== END ======{RESET}")
"""


class argsOPMaper:
    def __init__(self, parser) -> None:
        self.parser = parser
        self.args = parser.parse_args()
        self._caesar_ = {"caesar", "caesar_cipher", "caesarcipher"}
        self._more_ = {"mores", "mores_cipher", "morescipher", "mores-cipher"}
        self._playfair_ = {"playfaircipher", "playfair"}

        self._secure_ = False

    def run(self):
        self.validator()

        if self.args.encrypt:
            status = self.encMapper()

        elif self.args.decrypt:
            status = self.decMapper()

        if status:
            logger.info(f"{DGREEN}====== END ======{RESET}")

    def handle_help(self):
        if not self.args or self.args.help:
            _banner_()
            self.parser.print_help()
            sys.exit(
                f"{CYAN}👉 Brutefore only supports non-cipher encrypted file{RESET}"
            )

    def validator(self):
        self.handle_help()
        if not self.args.input_file:
            sys.exit("The following arguments are required: -i/--input_file")
        if not any((self.args.encrypt, self.args.decrypt)):
            sys.exit(
                f"You need to specify operation: {DYELLOW}Encryption{RESET}/{DYELLOW}Decryption{RESET}"
            )

        if not os.path.exists(self.args.input_file):
            sys.exit(f"{BWHITE}File does not exist{RESET}")

        if not any(
            (
                self.args.random_key,
                self.args.passphrase,
                self.args.cipher,
                self.args.pass_list,
                self._secure_,
            )
        ):
            sys.exit(
                "An encryption passphrase is needed otherwise try the command again with '--Rk' flag to use a randomly generated encryption key"
            )
        return True

    @staticmethod
    def get_keys(pf) -> list[str]:
        with open(pf) as f:
            ps = f.read()
        return ps.split(",")

    def multiLevelEnc(self, pass_list, isfile=True):
        def _exec(file, key):
            if isfile:
                enc_control(file, self.args.cipher, key)
            else:
                init = HandleFolders(file, key)
                init.encrypt_folder()

        e_level = 0

        input_file = self.args.input_file
        for pass_key in pass_list:
            _exec(input_file, pass_key)
            input_file = (
                f"{input_file}" f".enc{e_level}"
                if input_file[-4:-1] != "enc"
                else f"{input_file[:-1]}" f"{e_level}"
            )

            e_level += 1

        # Clean intermediary files
        _clean_Origfile_(input_file)

    def multiLevelDec(self, pass_list, isfile=True):
        def _exec(file, key):
            if isfile:
                dec_control(file, self.args.cipher, key)
            else:
                init = HandleFolders(file, key)
                init.decrypt_folder()

        e_level = 0

        input_file = self.args.input_file
        for pass_key in pass_list:
            _exec(input_file, pass_key)
            input_file = (
                f"{input_file}" f".enc{e_level}"
                if input_file[-4:-1] != "enc"
                else f"{input_file[:-1]}" f"{e_level}"
            )

            e_level += 1

        # Clean intermediary files
        clean_Encfile(input_file)

    """Hnadle All Encryption operations"""

    def encMapper(self):
        _map = {
            self.args.cipher: self.cipherEnc,
            os.path.isfile(self.args.input_file)
            and any((self.args.passphrase, self.args.pass_list)): self.encFile,
            os.path.isdir(self.args.input_file)
            and any((self.args.passphrase, self.args.pass_list)): self.encDir,
        }
        method = next((_map[key] for key in _map if key), None)
        if method:
            status = method()
            if status:
                logger.info(f"Encryption {DGREEN}Done")
                return True

    def cipherEnc(self):
        logger.info(
            f"{DGREEN}======START@Encryption:{DYELLOW}Target:{BLUE}Dir{GREEN}======{RESET}"
        )

        def validate():
            if self.args.cipher not in (
                self._caesar_.union(self._more_, self._playfair_)
            ):
                logger.setLevel("CRITICAL")
                logger.critical(f"\033[95m{self.args.cipher}\033[0m cipher not found")
                sys.exit(2)

            if not self.args.passphrase and self.args.cipher.lower() in self._playfair_:
                sys.exit("Please provide passphrase")

            return True

        try:
            if validate():
                if self.args.cipher.lower() in set(self._more_):
                    _enc_control_(self.args.input_file)
                elif self.args.cipher.lower() in set(self._caesar_):
                    enc_control(self.input_file, cipher=None, key=None)

                elif self.args.pass_list:
                    self.multiLevelEnc(
                        self.get_keys(self.args.pass_list)
                        if os.path.exists(self.args.pass_list)
                        else list(self.args.pass_list)
                    )
                elif self.args.passphrase:
                    logger.info(f"{BWHITE}@key={CGREEN}{self.passphrase}{RESET}")
                    enc_control(self.input_file, self.args.cipher, self.args.passphrase)
                    return True
        except Exception:
            return False

    def encFile(self):
        logger.info(f"{DGREEN}======START@Encryption======{RESET}")
        try:
            if self.args.pass_list:
                self.multiLevelEnc(
                    self.get_keys(self.args.pass_list)
                    if os.path.exists(self.args.pass_list)
                    else list(self.args.pass_list)
                )
            elif self.args.passphrase:
                init = HandleFiles(self.args.input_file, self.args.passphrase)
                init.encrypt_file()

            # Handle case where passphrase is not provided but random key is provided

            elif self.args.random_key:
                encrypt_file(self.args.input_file)
        finally:
            pass  # _clean_Origfile_(self.args.input_file)

    def encDir(self):
        logger.info(f"{DGREEN}======START@{BLUE}DIR-{GREEN}Encryption======{RESET}")
        try:
            if self.args.pass_list:
                self.multiLevelEnc(
                    self.get_keys(self.args.pass_list)
                    if os.path.exists(self.args.pass_list)
                    else list(self.args.pass_list),
                    isfile=False,
                )
            elif self.args.passphrase:
                logger.info(
                    f"{BWHITE}@key length={CGREEN}{len(self.args.passphrase)}{RESET}"
                )
                init = HandleFolders(self.args.input_file, self.args.passphrase)
                init.encrypt_folder()

            # Handle case where passphrase is not provided but random key is provided

            elif self.args.random_key:
                encrypt_folder(self.args.input_file)
        finally:
            # Clean original files from the directory
            _clean_dir_(self.args.input_file, False)

    """Hnadle All Decryption operations"""

    def decMapper(self):
        _map = {
            self.args.cipher: self.cipherDec,
            self.args.bruteforce: self.BruteforceDec,
            os.path.isfile(self.args.input_file)
            and any((self.args.passphrase, self.args.pass_list)): self.decFile,
            os.path.isdir(self.args.input_file)
            and any((self.args.passphrase, self.args.pass_list)): self.decDir,
        }
        method = next((_map[key] for key in _map if key), None)
        if method:
            status = method()
            if status:
                logger.info(f"Decryption {DGREEN}Done")
                return True

    def BruteforceDec(self):
        init = Bruteforce(self.args.input_file, self.args.bruteforce)
        init.conservative()

    def cipherDec(self):
        logger.info(
            f"{DGREEN}======START@Decryption:{DYELLOW}Target:{BLUE}Dir{GREEN}======{RESET}"
        )

        def validate():
            if self.args.cipher not in (
                self._caesar_.union(self._more_, self._playfair_)
            ):
                logger.setLevel("CRITICAL")
                logger.critical(f"\033[95m{self.args.cipher}\033[0m cipher not found")
                sys.exit(2)

            if not self.args.passphrase and self.args.cipher.lower() in self._playfair_:
                sys.exit("Please provide passphrase")

            return True

        try:
            if validate():
                if self.args.cipher.lower() in set(self._more_):
                    _dec_control_(self.args.input_file)
                elif self.args.cipher.lower() in set(self._caesar_):
                    dec_control(self.input_file, cipher=None, key=None)

                elif self.args.pass_list:
                    self.multiLevelDec(
                        self.get_keys(self.args.pass_list)
                        if os.path.exists(self.args.pass_list)
                        else list(self.args.pass_list)
                    )
                elif self.args.passphrase:
                    logger.info(f"{BWHITE}@key={CGREEN}{self.passphrase}{RESET}")
                    dec_control(self.input_file, self.args.cipher, self.args.passphrase)
                    return True
        except Exception:
            return False

    def decFile(self):
        logger.info(f"{DGREEN}======START@Decryption======{RESET}")

        try:
            if self.args.pass_list:
                self.multiLevelDec(
                    self.get_keys(self.args.pass_list)
                    if os.path.exists(self.args.pass_list)
                    else list(self.args.pass_list)
                )
            elif self.args.passphrase:
                init = HandleFiles(self.args.input_file, self.args.passphrase)
                init.decrypt_file()

            # Handle case where passphrase is not provided but random key is provided

            elif self.args.random_key:
                decrypt_file(self.args.input_file)
        finally:
            pass  # _clean_Origfile_(self.args.input_file)

    def decDir(self):
        logger.info(f"{DGREEN}======START@{BLUE}DIR-{GREEN}Decryption======{RESET}")
        try:
            if self.args.pass_list:
                self.multiLevelEnc(
                    self.get_keys(self.args.pass_list)
                    if os.path.exists(self.args.pass_list)
                    else list(self.args.pass_list),
                    isfile=False,
                )
            elif self.args.passphrase:
                logger.info(
                    f"{BWHITE}@key length={CGREEN}{len(self.args.passphrase)}{RESET}"
                )
                init = HandleFolders(self.args.input_file, self.args.passphrase)
                init.decrypt_folder()

            # Handle case where passphrase is not provided but random key is provided

            elif self.args.random_key:
                decrypt_folder(self.args.input_file)
        finally:
            # Clean original files from the directory
            _clean_dir_(self.args.input_file, False)


if __name__ == "__main__":
    ArgsMain()
