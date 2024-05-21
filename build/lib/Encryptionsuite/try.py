import os


def clean(input_file):
    _orig_ = input_file
    for i in range(int(input_file[-1:]), -1, -1):
        file = f'{input_file[:-1]}{i}'
        while os.path.exists(file) and file != f'{input_file[:-1]}{_orig_[-1:]}':
            print(f"\033[2;35mDelete \033[1m{file}🚮\033[0m")
            os.remove(file)
            print(file)
            break


clean("file.txt.enc5")
