from saes import SimplifiedAES


class TripleSimplifiedAES_mode1(object):
    def __init__(self, key1, key2):
        self.aes1 = SimplifiedAES(key1)
        self.aes2 = SimplifiedAES(key2)

    def encrypt(self, plaintext):
        ciphertext1 = self.aes1.encrypt(plaintext)
        ciphertext2 = self.aes2.encrypt(ciphertext1)
        return ciphertext2

    def decrypt(self, ciphertext):
        decrypted1 = self.aes2.decrypt(ciphertext)
        decrypted2 = self.aes1.decrypt(decrypted1)
        return decrypted2


class TripleSimplifiedAES_mode2(object):
    def __init__(self, key1, key2, key3):
        self.aes1 = SimplifiedAES(key1)
        self.aes2 = SimplifiedAES(key2)
        self.aes3 = SimplifiedAES(key3)

    def encrypt(self, plaintext):
        ciphertext1 = self.aes1.encrypt(plaintext)
        ciphertext2 = self.aes2.encrypt(ciphertext1)
        ciphertext3 = self.aes3.encrypt(ciphertext2)
        return ciphertext3

    def decrypt(self, ciphertext):
        decrypted2 = self.aes3.decrypt(ciphertext)
        decrypted1 = self.aes2.decrypt(decrypted2)
        decrypted0 = self.aes1.decrypt(decrypted1)
        return decrypted0
def main():
    while True:
        choice = input("Choose an option: (e)ncrypt, (d)ecrypt, (q)uit: ").lower()
        if choice == 'q':
            break
        elif choice in ['e', 'd']:
            # 获取密钥
            key1 = int(input("Enter the first key (as a 4-digit hex number): "), 16)
            key2 = int(input("Enter the second key (as a 4-digit hex number): "), 16)
            if choice == 'e':
                key3 = int(input("Enter the third key (as a 4-digit hex number) for mode 2, or press enter for mode 1: "), 16) if choice == 'e' and key2 != 0 else 0
                if choice == 'e' and key3 == 0:
                    print("Mode 1 selected. No third key required.")
                else:
                    print("Mode 2 selected.")
                # 获取明文或密文
                plaintext = int(input("Enter the plaintext (as a 4-digit hex number): "), 16)
                if choice == 'e':
                    triple_aes = TripleSimplifiedAES_mode1(key1, key2) if key3 == 0 else TripleSimplifiedAES_mode2(key1, key2, key3)
                    ciphertext = triple_aes.encrypt(plaintext)
                    print(f"Ciphertext: {ciphertext:04X}")
                elif choice == 'd':
                    ciphertext = int(input("Enter the ciphertext (as a 4-digit hex number): "), 16)
                    triple_aes = TripleSimplifiedAES_mode1(key1, key2) if key3 == 0 else TripleSimplifiedAES_mode2(key1, key2, key3)
                    decrypted_plaintext = triple_aes.decrypt(ciphertext)
                    print(f"Decrypted Plaintext: {decrypted_plaintext:04X}")
            else:
                print("Invalid option. Please choose 'e' to encrypt or 'd' to decrypt.")
        else:
            print("Invalid option. Please choose 'e' to encrypt, 'd' to decrypt, or 'q' to quit.")

if __name__ == "__main__":
    main()