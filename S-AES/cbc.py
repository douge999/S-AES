from saes import SimplifiedAES
from zhuanhuan import decimal_to_16bit_binary
# 生成16位初始向量(IV)，双方共享
iv = 0b1100110011001100

def cbc_encrypt(plaintext, key, iv):
    ciphertext = []
    previous_cipher = iv
    saes = SimplifiedAES(key)

    for block in plaintext:
        # 在加密前，每个明文分组与前一个密文分组(或IV)进行异或操作
        xor_result = block ^ previous_cipher
        encrypted_block = saes.encrypt(xor_result)
        ciphertext.append(encrypted_block)
        previous_cipher = encrypted_block

    return ciphertext


def cbc_decrypt(ciphertext, key, iv):
    plaintext = []
    saes = SimplifiedAES(key)
    previous_cipher = iv

    for block in ciphertext:
        decrypted_block = saes.decrypt(block)
        # 在解密后，需要将解密结果与前一个密文分组(或IV)进行异或操作
        plaintext_block = decrypted_block ^ previous_cipher
        plaintext.append(plaintext_block)
        previous_cipher = block

    return plaintext


# 示例明文和密钥
plaintext = [0b1010101011011010, 0b1010010110011101, 0b1010110111011010, 0b1010100110011101]
key = 0b0100101011110101

# 加密
ciphertext = cbc_encrypt(plaintext, key, iv)

# 输出加密结果
print("Ciphertext:")
for block in ciphertext:
    print(decimal_to_16bit_binary(block))

# 修改第一个密文块
ciphertext[0] = 0b0000000000000000  # 替换第一个密文块

# 解密
decrypted_plaintext = cbc_decrypt(ciphertext, key, iv)

# 输出解密结果
print("Decrypted Plaintext:")
for block in decrypted_plaintext:
    print(decimal_to_16bit_binary(block))
