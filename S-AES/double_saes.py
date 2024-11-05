from saes import SimplifiedAES

class DoubleSimplifiedAES(object):
    def __init__(self, key):
        if not isinstance(key, int):
            raise ValueError("密钥必须是整数。")
        if key < 0 or key > 0xFFFFFFFF:
            raise ValueError("密钥必须是32位整数。")
        self.key = key
        self.key1 = (key & 0xFFFF0000) >> 16  # 密钥的高16位
        self.key2 = key & 0x0000FFFF  # 密钥的低16位
        self.aes1 = SimplifiedAES(self.key1)  # 使用key1创建第一个AES实例
        self.aes2 = SimplifiedAES(self.key2)  # 使用key2创建第二个AES实例

    def encrypt(self, plaintext):
        intermediate_result = self.aes1.encrypt(plaintext)  # 第一次加密
        ciphertext = self.aes2.encrypt(intermediate_result)  # 第二次加密
        return ciphertext

    def decrypt(self, ciphertext):
        intermediate_result = self.aes2.decrypt(ciphertext)  # 第二次解密
        plaintext = self.aes1.decrypt(intermediate_result)  # 第一次解密
        return plaintext
def main():
    # 用户输入
    while True:
        choice = input("Choose an option: (e)ncrypt, (d)ecrypt, (q)uit: ").lower()
        if choice == 'q':
            break
        elif choice in ['e', 'd']:
            # 获取密钥
            key = int(input("Enter the key (as a 8-digit hex number): "), 16)
            # 获取明文或密文
            if choice == 'e':
                plaintext = int(input("Enter the plaintext (as a 4-digit hex number): "), 16)
                double_aes = DoubleSimplifiedAES(key)
                ciphertext = double_aes.encrypt(plaintext)
                print(f"Ciphertext: {ciphertext:04X}")
            elif choice == 'd':
                ciphertext = int(input("Enter the ciphertext (as a 4-digit hex number): "), 16)
                double_aes = DoubleSimplifiedAES(key)
                decrypted_plaintext = double_aes.decrypt(ciphertext)
                print(f"Decrypted Plaintext: {decrypted_plaintext:04X}")
        else:
            print("Invalid option. Please choose 'e' to encrypt, 'd' to decrypt, or 'q' to quit.")

if __name__ == "__main__":
    main()