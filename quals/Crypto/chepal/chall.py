#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
from secret import flag

KEY = get_random_bytes(16)

def encrypt(pt, key):
    cipher = AES.new(key, AES.MODE_ECB)
    result = cipher.encrypt(pt)
    return result

def oracle(pt):
    randbit = getrandbits(4)
    pt = pad( pt + (b'A' * randbit) + flag, 16)

    return encrypt(pt, KEY).hex()

if __name__ == '__main__':
    while True:
        user_input = input("Input pesan untuk di encrypt : ")
        res = oracle(user_input.encode())
        print("Hasil encrypt : ")
        print(res)