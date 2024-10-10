import os

from .ciphers import CaesarCipher
from .colors import (BWHITE, CGREEN, FMAGENTA,
                     RED, RESET, YELLOW, FBLUE)

mapping = {"\\": "✴️",
           "/": "❇️",
           ".": "⏹️",
           "A": ".",
           "B": "..",
           "C": "...",
           "D": "....",
           "E": ".....",
           "F": "......",
           "G": ".......",
           "H": "........",
           "I": ".........",
           "J": "..........",
           "K": "...........",
           "L": "............",
           "M": ".............",
           "N": "..............",
           "O": "...............",
           "P": "................",
           "Q": ".................",
           "R": "..................",
           "S": "...................",
           "T": "....................",
           "U": ".....................",
           "V": "......................",
           "W": ".......................",
           "X": "........................",
           "Y": ".........................",
           "Z": ".........................."
           }


def mapv(caesarv, f=None):
    result = ""
    unmap = ''
    print(f"{YELLOW}Initiate map sequence{RESET}")
    for char in caesarv:
        mapped = False
        for key, value in mapping.items():
            # print(f"\033[95mMap: {key}{RESET}", end='\r')
            if key == char:
                result += value + '~' + '/'
                mapped = True
                break
            elif not mapped and key.lower() == char:
                result += value + '/'
                mapped = True
                break
        if not mapped:
            unmap += char
            result += char + '/'
        info = f"({FMAGENTA}{unmap}{RESET})->\033[91mnot mapped {YELLOW}but no panic{RESET}" if f is True else f"INFO\t {FBLUE}{len(unmap)}{CGREEN} unmapped/ignored characters{RESET}"
    print(info)
    if result.endswith('/'):
        result = result[:-1]
    # print(f"\033[92m{result}{RESET}")
    return result


def Reverse_mapping(mapv, f=None):
    st = mapv.split('/')
    unmap = ''
    string = ''
    print(F"{YELLOW}Initiate unmap sequence{RESET}")
    for val in st:
        found = False
        for key, value in mapping.items():
            # print(f"\033[95mUnmap\033[0;1m: {value}{RESET}", end='\r')
            if value == val:
                string += key.lower()
                found = True
                break
            elif not found and value == val.replace('~', ''):
                string += key
                found = True
                break
        if not found:
            unmap += val
            string += val
    info = f"({FMAGENTA}{unmap}{RESET})->\033[91mnot found {YELLOW}but no panic{RESET}" if f is True else f"INFO\t {FBLUE}{len(unmap)}{CGREEN} unmapped/ignored characters{RESET}"

    print(info)

    return string


def _enc_control_(input_file):
    try:
        if os.path.isfile(input_file):
            f = True
            # Open and read file data
            with open(input_file, 'r') as f:
                data = f.read()
        else:
            data = mapv
            f = False

        ed = CaesarCipher(data)
        caesar = ed.encode()
        data = mapv(caesar, f)

        # Generator output file name
        file = input_file
        e_level = int(file[-1:]) + 1 if file[-4:-1] == 'enc' else 0
        _out_fname_ = f'{file[:-1]}{e_level}' if file[-4:-
                                                      1] == 'enc' else f'{file}.enc{e_level}'

    except KeyboardInterrupt:
        print("\nQuit❕")
    except FileExistsError as e:
        print(f"{RED}{e}{RESET}")
    except Exception as e:
        print(f"{RED}{e}{RESET}")
    finally:
        # Write the encrypted data to file
        with open(_out_fname_, 'w') as f:
            f.write(data)

        print(f"{BWHITE}File saved as {_out_fname_}")

        _path_ = input_file
        if os.path.exists(_path_ + f'.enc{0}') or os.path.exists(_path_ + f'.enc{1}'):
            print(f"{FMAGENTA}Delete {BWHITE}{_path_}🚮{RESET}")
            os.remove(_path_)
    return _out_fname_


def _dec_control_(_input_):
    try:
        if os.path.isfile(_input_):
            f = True
            # Open and read file data
            with open(_input_, 'r') as f:
                data = f.read()
        else:
            f = False
            data = mapv

        caesar = Reverse_mapping(data)
        ed = CaesarCipher(caesar)
        data = ed.decode()
        # Decide on output file name
        print(F"{FMAGENTA}Restore file name{RESET}")
        e_level = int(_input_[-1:]) - 1 if _input_[-4:-
                                                   1] == 'enc' and int(_input_[-1:]) != 0 else ''
        fname = f'{_input_[:-1]}{e_level}' if e_level != '' else _input_[:-5]
        with open(fname, 'w') as f:
            f.write(data)
        print(f"{BWHITE}File saved as {fname}")

    except KeyboardInterrupt:
        print("\nQuit❕")
    except FileExistsError as e:
        print(f"{RED}{e}{RESET}")
    except Exception as e:
        print(f"{RED}{e}{RESET}")
    finally:
        _path_ = _input_
        if os.path.exists(_path_[:-1] + f'{0}') or os.path.exists(_path_[:-1] + f'{1}') or os.path.exists(_path_[:-1] + f'{2}'):
            print(f"{FMAGENTA}Delete {BWHITE}{_path_}🚮{RESET}")
            os.remove(_path_)
    return fname


if __name__ == "__main__":
    ms = "/home/skye/Documents/draft/output/Resume.txt.enc0"
    _dec_control_(ms)
    '''choice = int(input("{YELLOW}encode/decode (1 or 2)??{RESET}:"))
    message = input("Enter your message:")

    if choice == 1:
        ed = CaesarCipher(message)
        caesar = ed.encode()
        mapv(caesar)

    elif choice == 2:
        caesar = Reverse_mapping(message)
        ed = CaesarCipher(caesar)
        ms = ed.decode()
        print(ms)'''
