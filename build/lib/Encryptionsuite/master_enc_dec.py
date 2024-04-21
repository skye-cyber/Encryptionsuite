
class PlayfairCipher:
    def __init__(self, data, key):
        self.data = data.upper().replace('J', 'I')
        self.key = key.upper().replace('J', 'I')

    @staticmethod
    def prepare_key(key):
        key_list = list(key)
        for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
            if char not in key_list:
                key_list.append(char)
        return ''.join(key_list)

    @staticmethod
    def create_matrix(key):
        matrix = [[''] * 5 for _ in range(5)]
        key_list = list(key)
        for i in range(5):
            for j in range(5):
                matrix[i][j] = key_list.pop(0)
        return matrix

    def encrypt(self):
        plaintext = self.data
        key = self.key
        """
        Encrypts the plaintext using the Playfair Cipher.
        Preserves the case of the original plaintext.
        """
        prepared_key = PlayfairCipher.prepare_key(key)
        matrix = PlayfairCipher.create_matrix(prepared_key)
        ciphertext = ""
        plaintext_list = list(plaintext)
        for i in range(0, len(plaintext_list), 2):
            pair = ''.join(plaintext_list[i:i+2])
            if len(pair) < 2:
                pair += 'X'
            row1, col1 = None, None
            row2, col2 = None, None
            for j in range(5):
                for k in range(5):
                    if matrix[j][k] == pair[0]:
                        row1, col1 = j, k
                    elif matrix[j][k] == pair[1]:
                        row2, col2 = j, k
            if row1 == row2:
                ciphertext += matrix[row1][(col1+1) %
                                           5] + matrix[row2][(col2+1) % 5]
            elif col1 == col2:
                ciphertext += matrix[(row1+1) % 5][col1] + \
                    matrix[(row2+1) % 5][col2]
            else:
                ciphertext += matrix[row1][col2] + matrix[row2][col1]
        return ciphertext.lower()

    def decrypt(self):
        ciphertext = self.data
        key = self.key
        """
            Decrypts the ciphertext using the Playfair Cipher.
            Preserves the case of the original plaintext.
            """
        prepared_key = PlayfairCipher.prepare_key(key)
        matrix = PlayfairCipher.create_matrix(prepared_key)
        plaintext = ""
        ciphertext_list = list(ciphertext)
        for i in range(0, len(ciphertext_list), 2):
            pair = ''.join(ciphertext_list[i:i+2])
            row1, col1 = None, None
            row2, col2 = None, None
            for j in range(5):
                for k in range(5):
                    if matrix[j][k] == pair[0]:
                        row1, col1 = j, k
                    elif matrix[j][k] == pair[1]:
                        row2, col2 = j, k
            if row1 == row2:
                plaintext += matrix[row1][(col1-1) %
                                          5] + matrix[row2][(col2-1) % 5]
            elif col1 == col2:
                plaintext += matrix[(row1-1) % 5][col1] + \
                    matrix[(row2-1) % 5][col2]
            else:
                plaintext += matrix[row1][col2] + matrix[row2][col1]
            # Replace placeholder X with original value
            f_result = ""
            for i in range(len(plaintext)):
                if i == 0 or plaintext[i] != 'X':
                    f_result += plaintext[i]
                else:
                    f_result += plaintext[i-1]
            return f_result.lower()


if __name__ == "__main__":
    # PlayfairCipher
    key = "PLAYFAIREXAMPLE"
    plaintext = "Hello, World!"
    cipher = PlayfairCipher(plaintext, key)
    ciphertext = cipher.encrypt()
    print("Plaintext:", plaintext)
    print("Ciphertext:", ciphertext)
    cipher = PlayfairCipher(ciphertext, key)
    plaintext = cipher.decrypt()
    print("Decrypted data:", plaintext)
