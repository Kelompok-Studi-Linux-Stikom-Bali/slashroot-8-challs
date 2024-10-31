from Crypto.Cipher import AES as A
from Crypto.Cipher import AES 
import os as o
from tqdm import tqdm
from pwn import *

# r = process(["python3", "chall.py"])
r = remote("157.230.251.184", 10011)
tes = b""
for i in tqdm(range(256)):
    for j in range(256):
        r.sendlineafter(b": ", bytes([i, j]).hex().encode())
        temp = r.recvline(0)
        # print(i,j)
        if b"tidak valid" not in temp and b"slashroot" in temp:
            print(temp)
            # r.interactive()
r.interactive()