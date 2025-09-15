# Nama      : Raymond Frans Dodi Situmorang
# NPM       : 140810230030
# Kelas     : B
# Deskripsi : Membuat encrypt dan decrypt dari algoritma Vigenere cipher

def char_to_num(c):
    return ord(c.upper()) - ord('A')

def num_to_char(n):
    return chr((n % 26) + ord('A'))

def encrypt(plaintext, key):
    plaintext = plaintext.replace(" ", "")
    key = key.upper()
    ciphertext = ""
    index = 0

    for char in plaintext:
        if char.isalpha():
            pi = char_to_num(char)
            ki = char_to_num(key[index % len(key)])
            ci = (pi + ki) % 26
            ciphertext += num_to_char(ci)
            index +=1
        else:
            ciphertext += char
    return ciphertext

def decrypt(ciphertext, key):
    key = key.upper()
    plaintext = ""
    index = 0

    for char in ciphertext:
        if char.isalpha():
            ci = char_to_num(char)
            ki = char_to_num(key[index % len(key)])
            pi = (ci - ki) % 26
            plaintext += num_to_char(pi)
            index +=1
        else:
            plaintext += char
    return plaintext

plaintext = "ASPRAKGANTENG"
key = "RAY"

ciphertext = encrypt(plaintext, key)
print("Plaintext : ", plaintext)
print("Ciphertext : ", ciphertext)
decrypted = decrypt(ciphertext, key)
print("Decrypted : ", decrypted)