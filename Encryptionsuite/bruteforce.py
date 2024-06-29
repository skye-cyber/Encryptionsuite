import os

from master_ED import HandleFiles

# import pyperclip


class Bruteforce:
    def __init__(self, obj, dict_file):
        self.obj = obj
        self.dict_file = dict_file

    def conservative(self):
        # Critical redundacy
        # Goal:-> Is to avoid loosing the original files by Creating temporary directory to store temporary files
        if os.path.isfile(self.obj):
            try:
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
                passw = list(passw)
                # pass_ls = ['hello', "pass", "password", "passrr", "hhhh"]
                for key in passw:
                    key = key.strip('\n')
                    # print(f"\033[1;30m{key}\033[0m", end='')
                    # Create decryption object
                    init = HandleFiles(_fpath, key)
                    init.decrypt_file()
            except FileExistsError:
                pass

        elif os.path.isdir(self.obj):
            _path = os.path.dirname(self.obj)
            _dir = os.path.join(_path, "CRDIR")
            # Create temporary directory
            os.mkdir(_dir)
            cmd = f"cp -r {self.obj} {_dir}"
            os.system(cmd)

            # Open dictionary file for Bruteforce
            with open(self.dict_file, 'r') as df:
                passw = df.readlines()
            for root, dirs, files in os.walk(_dir):
                for file in files:
                    if file[:-1].endswith("enc"):
                        _path = os.path.join(root, file)
                        for key in passw:
                            key = key.strip()
                            # print(f"\033[1;30m{key}\033[0m", end='\r')
                            # Create decryption object
                            init = HandleFiles(_path, key)
                            init.decrypt_file()


init = Bruteforce("/home/skye/Documents/AReport.docx.enc0",
                  "/home/skye/Documents/john.lst")
init.conservative()
