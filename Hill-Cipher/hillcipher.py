import numpy as np

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def text_to_numbers(text):
    return [char_to_num(c) for c in text if c.isalpha()]

def numbers_to_text(nums):
    return ''.join(num_to_char(n) for n in nums)

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_mod_inv(matrix, modulus):
    n = matrix.shape[0]
    # determinan integer
    det = int(round(np.linalg.det(matrix))) % modulus
    det_inv = mod_inverse(det, modulus)
    if det_inv is None:
        raise ValueError("Determinant tidak punya invers modulo, matriks tidak valid!")

    # matriks cofaktor
    cofactors = np.zeros((n, n), dtype=int)
    for r in range(n):
        for c in range(n):
            minor = np.delete(np.delete(matrix, r, axis=0), c, axis=1)
            cof = int(round(np.linalg.det(minor)))
            cofactors[r, c] = ((-1) ** (r + c)) * cof

    # adjugate = transpose dari cofactor
    adjugate = cofactors.T % modulus

    # inverse = det_inv * adjugate mod modulus
    return (det_inv * adjugate) % modulus

def hill_encrypt(plaintext, key):
    n = len(key)
    P = text_to_numbers(plaintext)

    # padding X kalau tidak habis dibagi n
    while len(P) % n != 0:
        P.append(char_to_num('X'))

    C = []
    for i in range(0, len(P), n):
        block = np.array(P[i:i+n])
        enc_block = np.dot(key, block) % 26
        C.extend(enc_block)
    return numbers_to_text(C)

def hill_decrypt(ciphertext, key):
    n = len(key)
    C = text_to_numbers(ciphertext)
    key_inv = matrix_mod_inv(key, 26)

    P = []
    for i in range(0, len(C), n):
        block = np.array(C[i:i+n])
        dec_block = np.dot(key_inv, block) % 26
        P.extend(dec_block)
    return numbers_to_text(P)

def find_key(plaintext, ciphertext, n):
    P = text_to_numbers(plaintext[:n*n])
    C = text_to_numbers(ciphertext[:n*n])

    Mp = np.array(P).reshape(n, n).T
    Mc = np.array(C).reshape(n, n).T

    Mp_inv = matrix_mod_inv(Mp, 26)
    key = (np.dot(Mc, Mp_inv)) % 26
    return key

if __name__ == "__main__":
    key_matrix = np.array([[7, 8],
                           [19, 3]])

    plaintext = "FRIDAY"
    print("Plaintext :", plaintext)

    ciphertext = hill_encrypt(plaintext, key_matrix)
    print("Ciphertext:", ciphertext)

    decrypted = hill_decrypt(ciphertext, key_matrix)
    print("Decrypted :", decrypted)

    key_found = find_key(plaintext, ciphertext, 2)
    print("Key Found:\n", key_found)
