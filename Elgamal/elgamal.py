# Nama      : Raymond Frans Dodi Situmorang
# NPM       : 140810230030
# Kelas     : B
# Deskripsi : Membuat encrypt dan decrypt dari algoritma Elgamal

import random

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def encrypt(plaintext, p, g, y, k):
    ciphertext = []
    C_1 = pow(g, k, p)
    
    for char in plaintext:
        m = char_to_num(char)
        C_2 = (pow(y, k, p) * m) % p
        ciphertext.append((C_1, C_2))
    return ciphertext

def decrypt(ciphertext, p, x):
    plaintext = ""
    for (C_1, C_2) in ciphertext:
        C_1_x = pow(C_1, x, p)
        C_1_x_inv = mod_inverse(C_1_x, p)
        m = (C_2 * C_1_x_inv) % p
        plaintext += num_to_char(m)
    return plaintext

primes = [prima for prima in range(29, 500) if is_prime(prima)]
p = random.choice(primes)

g = random.randint(1, p-1)
x = random.randint(1, p-2)
y = pow(g, x, p)

k = random.randint(1, p-2)


plaintext = "EZKRIPTOGRAFI"
print("Plaintext : ", plaintext)
print(f"p = {p}, g = {g}, x = {x}, y = {y}, k = {k}")

ciphertext = encrypt(plaintext, p, g, y, k)
print("ciphertext : ", ciphertext)

decrypted = decrypt(ciphertext, p, x)
print("decrypted : ", decrypted)