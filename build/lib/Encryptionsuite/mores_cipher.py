import os
from mciphers import CaesarCipher


mapping = {
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


def mapv(caesarv):
    result = ""
    unmap = ''
    print("\033[94mInitiate map sequence\033[0m")
    for char in caesarv:
        mapped = False
        for key, value in mapping.items():
           # print(f"\033[95mMap: {key}\033[0m", end='\r')
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
    print(f"(\033[1;96m{unmap}\033[0m)->\033[91mnot mapped \033[93mbut no panic\033[0m")
    if result.endswith('/'):
        result = result[:-1]
    # print(f"\033[92m{result}\033[0m")
    return result


def Reverse_mapping(mapv):
    st = mapv.split('/')
    unmap = ''
    string = ''
    print("\033[94mInitiate unmap sequence\033[0m")
    for val in st:
        found = False
        for key, value in mapping.items():
            # print(f"\033[95mUnmap\033[0;1m: {value}\033[0m", end='\r')
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

    print(f"(\033[1;96m{unmap}\033[0m)->\033[91mnot found \033[93mbut no panic\033[0m")

    return string


def _enc_control_(input_file):
    try:
        # Open and read file data
        with open(input_file, 'r') as f:
            data = f.read()
        ed = CaesarCipher(data)
        caesar = ed.encode()
        data = mapv(caesar)

        # Generator output file name
        file = input_file
        e_level = int(file[-1:]) + 1 if file[-4:-1] == 'enc' else 0
        _out_fname_ = f'{file[:-1]}{e_level}' if file[-4:-1] == 'enc' else f'{file}.enc{e_level}'

    except KeyboardInterrupt:
        print("\nQuit❕")
    except FileExistsError as e:
        print(f"\033[31m{e}\033[0m")
    except Exception as e:
        print(f"\033[31m{e}\033[0m")
    finally:
        # Write the encrypted data to file
        with open(_out_fname_, 'w') as f:
            f.write(data)

        print(f"\033[1mFile saved as{_out_fname_}")

        _path_ = input_file
        if os.path.exists(_path_ + f'.enc{0}') or os.path.exists(_path_ + f'.enc{1}'):
            print(f"\033[2;35mDelete \033[1m{_path_}🚮\033[0m")
            os.remove(_path_)
    return _out_fname_


def _dec_control_(input_file):
    try:
        # Open and read file data
        with open(input_file, 'r') as f:
            data = f.read()
        caesar = Reverse_mapping(input_file)
        ed = CaesarCipher(caesar)
        data = ed.decode()
        # Decide on output file name
        print("\033[1;35mRestore file name\033[0m")
        e_level = int(input_file[-1:]) - 1 if input_file[-4:-1] == 'enc' and int(input_file[-1:]) != 0 else ''
        fname = f'{input_file[:-1]}{e_level}' if e_level != '' else input_file[:-5]
        with open(fname, 'w') as f:
            f.write(data)
        print(f"\033[1mFile saved as{fname}")

    except KeyboardInterrupt:
        print("\nQuit❕")
    except FileExistsError as e:
        print(f"\033[31m{e}\033[0m")
    except Exception as e:
        print(f"\033[31m{e}\033[0m")
    finally:
        _path_ = input_file
        if os.path.exists(_path_[:-1] + f'{0}') or os.path.exists(_path_[:-1] + f'{1}') or os.path.exists(_path_[:-1] + f'{2}'):
            print(f"\033[2;35mDelete \033[1m{_path_}🚮\033[0m")
            os.remove(_path_)
    return fname


if __name__ == "__main__":
    ms = "/home/skye/Documents/draft/output/test"
    _enc_control_(ms)
    '''choice = int(input("\033[93mencode/decode (1 or 2)??\033[0m:"))
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
