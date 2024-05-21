class VigenereCipher:
    def __init__(self, key, handle_non_alpha='ignore', preserve_case=False):
        self.key = key.upper()
        self.handle_non_alpha = handle_non_alpha
        self.preserve_case = preserve_case

    def encrypt(self, plaintext):
        """
        Encrypts the given plaintext using the Vigenère cipher.

        Args:
            plaintext (str): The text to be encrypted.

        Returns:
            str: The encrypted ciphertext.
        """
        if not plaintext:
            raise ValueError("Plaintext cannot be empty.")

        ciphertext = ""
        key_len = len(self.key)
        for i, char in enumerate(plaintext):
            if char.isalpha():
                if self.preserve_case:
                    char_case = 'A' if char.isupper() else 'a'
                else:
                    char = char.upper()
                    char_case = 'A'

                key_char = self.key[i % key_len]
                shifted_char = (ord(char) + ord(key_char)) % 26
                ciphertext += chr(shifted_char + ord(char_case))
            else:
                if self.handle_non_alpha == 'include':
                    ciphertext += char

        return ciphertext

    def decrypt(self, ciphertext):
        """
        Decrypts the given ciphertext using the Vigenère cipher.

        Args:
            ciphertext (str): The text to be decrypted.

        Returns:
            str: The decrypted plaintext.
        """
        if not ciphertext:
            raise ValueError("Ciphertext cannot be empty.")

        plaintext = ""
        key_len = len(self.key)
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                if self.preserve_case:
                    char_case = 'A' if char.isupper() else 'a'
                else:
                    char = char.upper()
                    char_case = 'A'

                key_char = self.key[i % key_len]
                shifted_char = (ord(char) - ord(key_char)) % 26
                plaintext += chr(shifted_char + ord(char_case))
            else:
                if self.handle_non_alpha == 'include':
                    plaintext += char

        return plaintext


if __name__ == "__main__":
    # Example usage
    cipher = VigenereCipher(
        key="PYTHON", handle_non_alpha='include', preserve_case=True)
    plaintext = "Hello, World!"
    ciphertext = cipher.encrypt(plaintext)
    # Output: Encrypted text: Hqnqo, Xprld!
    print("Encrypted text:", ciphertext)
    decrypted_text = cipher.decrypt(ciphertext)
    # Output: Decrypted text: Hello, World!
    print("Decrypted text:", decrypted_text)
