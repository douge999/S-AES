class SimplifiedAES(object):
    # (保持不变的代码部分省略)
    # S-Box and Inverse S-Box
    S_BOX = [
        0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5, 0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7
    ]
    INVERSE_S_BOX = [
        0xA, 0x5, 0x9, 0xB, 0x1, 0x7, 0x8, 0xF, 0x6, 0x0, 0x2, 0x3, 0xC, 0x4, 0xD, 0xE
    ]

    def __init__(self, key):
        """Initialize SimplifiedAES with the given key."""
        self.pre_round_key, self.round1_key, self.round2_key = self.key_expansion(key)

    def substitute_word(self, word):
        """Substitute word using S-Box."""
        return (self.S_BOX[(word >> 4)] << 4) + self.S_BOX[word & 0x0F]

    def rotate_word(self, word):
        """Rotate word by swapping its nibbles."""
        return ((word & 0x0F) << 4) + ((word & 0xF0) >> 4)

    def find_key(self, plaintext, ciphertext):
        for key_guess in range(0x10000):
            state = self.add_round_key(self.int_to_state(plaintext), self.int_to_state(key_guess))
            state = self.substitute_nibbles(self.S_BOX, self.shift_rows(state))
            state = self.mix_columns(state)

            if self.state_to_int(state) == ciphertext:
                return key_guess

        return None

    def key_expansion(self, key):
        """Expand the given key into round keys for encryption and decryption."""
        # Constants for key expansion
        RCON1 = 0x80
        RCON2 = 0x30

        # Extracting individual bytes from the key
        w = [None] * 6
        w[0] = (key & 0xFF00) >> 8
        w[1] = key & 0x00FF
        w[2] = w[0] ^ (self.substitute_word(self.rotate_word(w[1])) ^ RCON1)
        w[3] = w[2] ^ w[1]
        w[4] = w[2] ^ (self.substitute_word(self.rotate_word(w[3])) ^ RCON2)
        w[5] = w[4] ^ w[3]

        return (
            self.int_to_state((w[0] << 8) + w[1]),  # Pre-Round key
            self.int_to_state((w[2] << 8) + w[3]),  # Round 1 key
            self.int_to_state((w[4] << 8) + w[5])  # Round 2 key
        )

    @staticmethod
    def galois_field_multiply(a, b):
        """Galois field multiplication of a and b in GF(2^4) / x^4 + x + 1"""
        product = 0

        a = a & 0x0F
        b = b & 0x0F

        while a and b:
            if b & 1:
                product ^= a
            a = a << 1
            if a & (1 << 4):
                a ^= 0b10011
            b = b >> 1

        return product

    @staticmethod
    def int_to_state(n):
        """Convert a 2-byte integer into a 4-element vector (state matrix)."""
        return [n >> 12 & 0xF, (n >> 4) & 0xF, (n >> 8) & 0xF, n & 0xF]

    @staticmethod
    def state_to_int(state):
        """Convert a 4-element vector (state matrix) into a 2-byte integer."""
        return (state[0] << 12) + (state[2] << 8) + (state[1] << 4) + state[3]

    @staticmethod
    def add_round_key(state, round_key):
        """Add round keys in GF(2^4)."""
        return [i ^ j for i, j in zip(state, round_key)]

    def substitute_nibbles(self, sbox, state):
        """Nibble substitution using the specified S-Box."""
        return [sbox[nibble] for nibble in state]

    def shift_rows(self, state):
        """Shift rows and inverse shift rows of state matrix (same)."""
        return [state[0], state[1], state[3], state[2]]

    def mix_columns(self, state):
        """Mix columns transformation on state matrix."""
        return [
            state[0] ^ self.galois_field_multiply(4, state[2]),
            state[1] ^ self.galois_field_multiply(4, state[3]),
            state[2] ^ self.galois_field_multiply(4, state[0]),
            state[3] ^ self.galois_field_multiply(4, state[1]),
        ]

    def inverse_mix_columns(self, state):
        """Inverse mix columns transformation on state matrix."""
        return [
            self.galois_field_multiply(9, state[0]) ^ self.galois_field_multiply(2, state[2]),
            self.galois_field_multiply(9, state[1]) ^ self.galois_field_multiply(2, state[3]),
            self.galois_field_multiply(9, state[2]) ^ self.galois_field_multiply(2, state[0]),
            self.galois_field_multiply(9, state[3]) ^ self.galois_field_multiply(2, state[1]),
        ]

    def encrypt(self, plaintext):
        """Encrypt the given 16-bit plaintext."""
        state = self.add_round_key(self.pre_round_key, self.int_to_state(plaintext))
        state = self.mix_columns(self.shift_rows(self.substitute_nibbles(self.S_BOX, state)))
        state = self.add_round_key(self.round1_key, state)
        state = self.shift_rows(self.substitute_nibbles(self.S_BOX, state))
        state = self.add_round_key(self.round2_key, state)
        return self.state_to_int(state)

    def decrypt(self, ciphertext):
        """Decrypt the given 16-bit ciphertext."""
        state = self.add_round_key(self.round2_key, self.int_to_state(ciphertext))
        state = self.substitute_nibbles(self.INVERSE_S_BOX, self.shift_rows(state))
        state = self.inverse_mix_columns(self.add_round_key(self.round1_key, state))
        state = self.substitute_nibbles(self.INVERSE_S_BOX, self.shift_rows(state))
        state = self.add_round_key(self.pre_round_key, state)
        return self.state_to_int(state)

def ascii_to_int(ascii_str):
    """Convert a 2-character ASCII string to a 16-bit integer."""
    if len(ascii_str) != 2:
        raise ValueError("Input string must be 2 characters.")
    return (ord(ascii_str[0]) << 8) + ord(ascii_str[1])

def int_to_ascii(num):
    """Convert a 16-bit integer back to a 2-character ASCII string."""
    return chr((num >> 8) & 0xFF) + chr(num & 0xFF)

def main():
    # 用户输入
    while True:
        choice = input("Choose an option: (e)ncrypt, (d)ecrypt, (q)uit: ").lower()
        if choice == 'q':
            break
        elif choice in ['e', 'd']:
            # 获取密钥
            key = int(input("Enter the key (as a 4-digit hex number): "), 16)
            # 获取明文或密文
            if choice == 'e':
                plaintext = input("Enter the plaintext (2 characters): ")
                # 将 ASCII 字符串转换为整数
                plaintext_int = ascii_to_int(plaintext)
                aes = SimplifiedAES(key)
                ciphertext = aes.encrypt(plaintext_int)
                print(f"Ciphertext: {ciphertext:04X}")
            elif choice == 'd':
                ciphertext = int(input("Enter the ciphertext (as a 4-digit hex number): "), 16)
                aes = SimplifiedAES(key)
                decrypted_plaintext_int = aes.decrypt(ciphertext)
                decrypted_plaintext = int_to_ascii(decrypted_plaintext_int)
                print(f"Decrypted Plaintext: {decrypted_plaintext}")
        else:
            print("Invalid option. Please choose 'e' to encrypt, 'd' to decrypt, or 'q' to quit.")

if __name__ == "__main__":
    main()