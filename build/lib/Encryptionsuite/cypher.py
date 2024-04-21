class CaesarCipher:
    def __init__(self, key=8):
        """Initialize the Caesar Cipher object."""
        self.key = key
        # print(message)

    def encode(self, message):
        """Encode the given message using the provided key."""
        # print(self.message)
        result = ''
        for char in message:
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

    def decode(self, message):
        """Decode the given message using the provided key."""
        result = ''
        for char in message:
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
    for char in caesarv:
        mapped = False
        for key, value in mapping.items():
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
    print(f"\033[92m{result}\033[0m")
    # return cp


def Reverse_mapping(mapv):
    st = mapv.split('/')
    unmap = ''
    string = ''
    for val in st:
        found = False
        for key, value in mapping.items():
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

    # print(string)
    return string


if __name__ == "__main__":
    choice = int(input("\033[93mencode/decode (1 or 2)??\033[0m:"))
    ed = CaesarCipher()
    message = input("Enter your message:")
    if choice == 1:
        caesar = ed.encode(message)
        mapv(caesar)

    elif choice == 2:
        caesar = Reverse_mapping(message)
        ms = ed.decode(caesar)
        print(ms)
