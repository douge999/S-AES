def decimal_to_16bit_binary(decimal_num):
    """将十进制数转换为16位二进制数，并在左侧补零"""
    binary_str = bin(decimal_num)[2:]  # 将十进制数转换为二进制字符串并去除前缀'0b'
    if len(binary_str) < 16:
        padded_binary_str = '0' * (16 - len(binary_str)) + binary_str  # 在左侧补零
        return padded_binary_str
    elif len(binary_str) == 16:
        return binary_str
    else:
        raise ValueError("输入的十进制数太大，无法表示为16位二进制数")