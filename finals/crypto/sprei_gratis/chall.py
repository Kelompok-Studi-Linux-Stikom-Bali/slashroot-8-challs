#!/usr/bin/python3

from Crypto.Util.number import *
from base64 import urlsafe_b64encode
from hashlib import sha256
import secrets

SPREI = "slashroot{omke_gas}" if "SPREI" not in os.environ else os.environ['SPREI']

class OMKE_GAS:
    def __init__(self, bit):
        self.bit = bit
        self.p = getPrime(self.bit//2)
        self.q = getPrime(self.bit//2)
        self.n = self.p * self.q
        self.e = 0x10001
        self.d = inverse(self.e, (self.p-1)*(self.q-1))
    
    def fufufafa(self, x, y):
        a = x ^ (y >> 25)
        b = y ^ (x << 52) & ((1 << 64) - 1)
        a ^= ((b << 11) & ((1 << 64) - 1)) | 0xf0f0fAfAf0f0fAfA
        b ^= ((a >> 17) & ((1 << 64) - 1)) & 0xf4f4f4f4f0f0f0f0
        return a, b

    def makan_gratis(self, m):
        h = int(sha256(m.encode()).hexdigest(), 16)
        mp = pow(h, self.d % (self.p-1), self.p)
        mq = pow(h, self.d % (self.q-1), self.q)
        c = mq + self.q * ((mp - mq) * pow(self.q, -1, self.p) % self.p)
        a, b = self.fufufafa(mq >> ((self.bit//2)-64), secrets.randbits(64))
        return b'.'.join([urlsafe_b64encode(long_to_bytes(i)).strip(b'=') for i in [c, a, b]]).decode()
    
    def sprei_gratis(self, sprei):
        self.cipher = pow(bytes_to_long(sprei), self.e, self.n)
        return b'.'.join([urlsafe_b64encode(long_to_bytes(i)).strip(b'=') for i in [self.cipher, self.n]]).decode()    

chal = OMKE_GAS(1024)

print("plizzzz wokkk 😣😣😢😢 aku mau sprei gratis ibuku itu agak miskin 😭😭😭💔💔 kok saya liat livestream mu kenapa kamu ketawa hah 😡😡😡😡‼️‼️mana sprei gratis yang kau janjikan itu hah disaat pendukungmu oke gas oke gas 😝😝😝kamu malah ketawa 😂😂🤣 itu ga rizzpek banget wok😂😂 dan jangan lupa makanan siang gratisnya wok 😂😂😅😅😅")
print(f"Sprei gratis tapi dienkripsi fufufafa: {chal.sprei_gratis(SPREI)}")

while True:
    choice = int(input("Ketik 1 untuk dapat makan siang gratis: "))
    if choice == 1:
        m = input("Request lauk makan siang gratis: ")
        print(f"Vocer makan siang gratis tapi dienkripsi fufufafa: {chal.makan_gratis(m)}")
    else:
        break
