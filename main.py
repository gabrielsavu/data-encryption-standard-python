from multiprocessing.pool import ThreadPool
import re

PC1 = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]

PC2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

E_BIT_TABLE = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

S = [[
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
], [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
], [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
], [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
], [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
], [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
], [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]

], [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]]

P = [
    16, 7, 20, 21,
    29, 12, 28, 17,
    1, 15, 23, 26,
    5, 18, 31, 10,
    2, 8, 24, 14,
    32, 27, 3, 9,
    19, 13, 30, 6,
    22, 11, 4, 25
]

IP_INVERSE = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

SHIFTS_PER_IT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def rotate(bit_list, n):
    return bit_list[n:] + bit_list[:n]


def bit_list_to_string(bit_list: list, spacing_after: int):
    sb = ""
    for idx, bit in enumerate(bit_list):
        sb += str(bit)
        if (idx + 1) % spacing_after == 0:
            sb += " "

    return sb


def permute(permutation, bit_list):
    new_bit_list = [0] * len(permutation)
    for idx, val in enumerate(permutation):
        new_bit_list[idx] = bit_list[val - 1]

    return new_bit_list


def generate_sub_keys(key_bit_list: list):
    print(f"K = {bit_list_to_string(key_bit_list, 8)}")
    print("\n")

    key_plus_bit_list = permute(PC1, key_bit_list)
    print(f"K+ = {bit_list_to_string(key_plus_bit_list, 7)}")
    print("\n")

    c_bit_list = [key_plus_bit_list[:28]]
    d_bit_list = [key_plus_bit_list[28:]]

    print(f"C0 = {bit_list_to_string(c_bit_list[0], 7)}")
    print(f"D0 = {bit_list_to_string(d_bit_list[0], 7)}")
    print("\n")
    for i in range(1, 17):
        c_bit_list.append(rotate(c_bit_list[i - 1], SHIFTS_PER_IT[i - 1]))
        d_bit_list.append(rotate(d_bit_list[i - 1], SHIFTS_PER_IT[i - 1]))
        print(f"C{i} = {bit_list_to_string(c_bit_list[i], 7)}")
        print(f"D{i} = {bit_list_to_string(d_bit_list[i], 7)}")
        print("\n")

    sub_keys_bit_list = []
    for i in range(16):
        sub_keys_bit_list.append(permute(PC2, c_bit_list[i + 1] + d_bit_list[i + 1]))
        print(f"K{i} = {bit_list_to_string(sub_keys_bit_list[i], 6)}")

    return sub_keys_bit_list


def from_hex_string_to_bit_list(hex_string: str):
    integer = int(hex_string, 16)
    bit_string = format(integer, '0>64b')
    bit_list = re.findall('(\\d)', bit_string)
    return bit_list


def from_bit_list_to_hex_string(bit_list: list):
    binary = ''.join([str(i) for i in bit_list])
    hstr = '%0*X' % ((len(binary) + 3) // 4, int(binary, 2))
    return hstr


def from_string_to_bit_list(string):
    bit_list = re.findall('(\\d)', ' '.join(format(ord(x), '08b') for x in string))
    return bit_list


def from_int_to_4_bit_list(n):
    bit_list = re.findall('(\\d)', ' '.join(format(n, '04b')))
    return bit_list


def encode_64_bit_chunk_data(chunk_bit_list, sub_keys_bit_list):
    print("\n")
    print(f"M= {bit_list_to_string(chunk_bit_list, 4)}")
    ip_bit_list = permute(IP, chunk_bit_list)
    print(f"IP= {bit_list_to_string(ip_bit_list, 4)}")

    l_bit_list = [ip_bit_list[:32]]
    r_bit_list = [ip_bit_list[32:]]

    print(f"L0 = {bit_list_to_string(l_bit_list[0], 4)}")
    print(f"R0 = {bit_list_to_string(r_bit_list[0], 4)}")

    for i in range(1, 17):
        print(f"--- Round {i} ---")
        l_bit_list.append(r_bit_list[i - 1])
        r_bit_list.append(xor_bit_list(l_bit_list[i - 1], f(r_bit_list[i - 1], sub_keys_bit_list[i - 1])))
        print(f"L{i} = {bit_list_to_string(l_bit_list[i], 4)}")
        print(f"R{i} = {bit_list_to_string(r_bit_list[i], 4)}")

    ip_inverse_bit_list = permute(IP_INVERSE, r_bit_list[16] + l_bit_list[16])
    print("\n")
    print(f"IP^-1 = {bit_list_to_string(ip_inverse_bit_list, 8)}")
    return ip_inverse_bit_list


def f(r_bit_list, sub_key_bit_list):
    e_bit_list = permute(E_BIT_TABLE, r_bit_list)

    print(f"R = {bit_list_to_string(r_bit_list, 6)}")
    print(f"E(R) = {bit_list_to_string(e_bit_list, 6)}")

    ke_bit_list = xor_bit_list(sub_key_bit_list, e_bit_list)

    print(f"K = {bit_list_to_string(sub_key_bit_list, 6)}")

    print(f"KE = {bit_list_to_string(ke_bit_list, 6)}")
    n = 6
    b_bit_list = [ke_bit_list[i:i + n] for i in range(0, len(ke_bit_list), n)]

    s_box_bit_list = []
    for i in range(len(b_bit_list)):
        row = int(str(b_bit_list[i][0]) + str(b_bit_list[i][5]), 2)
        column = int(str(b_bit_list[i][1]) + str(b_bit_list[i][2]) + str(b_bit_list[i][3]) + str(b_bit_list[i][4]), 2)
        s_box_bit_list += from_int_to_4_bit_list(S[i][row][column])

    print(f"S_BOX = {bit_list_to_string(s_box_bit_list, 4)}")
    ps_box_bit_list = permute(P, s_box_bit_list)
    print(f"P(S_BOX) = {bit_list_to_string(ps_box_bit_list, 4)}")
    return ps_box_bit_list


def xor_bit_list(first_bit_list, second_bit_list):
    if len(first_bit_list) != len(second_bit_list):
        raise Exception("Length not equal")

    out_bit_list = []
    for i in range(len(first_bit_list)):
        out_bit_list.append(int(first_bit_list[i]) ^ int(second_bit_list[i]))

    return out_bit_list


def des(chunk_64_bit_list: list, sub_keys_bit_list: list):
    return encode_64_bit_chunk_data(chunk_64_bit_list, sub_keys_bit_list)


def des_ecb(text: str, key_hex: str):
    n = 8
    split_text = [text[i:i + n] for i in range(0, len(text), n)]

    key_bit_list = from_hex_string_to_bit_list(key_hex)
    sub_keys_bit_list = generate_sub_keys(key_bit_list)

    pool = ThreadPool(5)

    results = []
    for s in split_text:
        if len(s) != 8:
            s += '\0' * (8 - len(s))
        results.append(pool.apply_async(des, args=(
            from_hex_string_to_bit_list(s.encode("utf-8").hex()), sub_keys_bit_list)))

    pool.close()
    pool.join()

    results = [r.get() for r in results]

    bit_list = []
    for result in results:
        bit_list += result

    return from_bit_list_to_hex_string(bit_list)


def des_ecb_sync(text: str, key_hex: str):
    n = 8
    split_text = [text[i:i + n] for i in range(0, len(text), n)]

    key_bit_list = from_hex_string_to_bit_list(key_hex)
    sub_keys_bit_list = generate_sub_keys(key_bit_list)

    results = []
    for s in split_text:
        if len(s) != 8:
            s += '\0' * (8 - len(s))
        results += des(from_hex_string_to_bit_list(s.encode("utf-8").hex()), sub_keys_bit_list)

    return from_bit_list_to_hex_string(results)


def des_cbc(text: str, iv_hex: str, key_hex: str):
    n = 8
    split_text = [text[i:i + n] for i in range(0, len(text), n)]

    key_bit_list = from_hex_string_to_bit_list(key_hex)
    sub_keys_bit_list = generate_sub_keys(key_bit_list)

    print(f"IV = {from_hex_string_to_bit_list(iv_hex)}")

    results = []
    for i, s in enumerate(split_text):
        if len(s) != 8:
            s += '\0' * (8 - len(s))
        if i == 0:
            xor_input = xor_bit_list(from_hex_string_to_bit_list(iv_hex),
                                     from_hex_string_to_bit_list(s.encode("utf-8").hex()))
        else:
            xor_input = xor_bit_list(results[i - 1],
                                     from_hex_string_to_bit_list(s.encode("utf-8").hex()))

        results += [des(xor_input, sub_keys_bit_list)]

    bit_list = []
    for result in results:
        bit_list += result

    return from_bit_list_to_hex_string(bit_list)


def main():
    print('DES ECB: ' + des_ecb('HORST FEISTEL', '133457799BBCDFF1'))
    print('DES CBC: ' + des_cbc('HORST FEISTEL', '0' * 16, '133457799BBCDFF1'))


if __name__ == '__main__':
    main()
