from pwn import *

def send(ct):
    io.recv()
    io.sendline(bytes(ct).hex().encode())
    return io.recvline()[:-1]

# io = process(["python3", "./chall.py"])
io = remote('localhost', 10011)

ct = []
while len(ct) < 6:
    tmp = ct + [randint(0, 255)]
    print(tmp)
    pt = send(tmp)
    if all(i in b'123456789' for i in pt) and len(pt) == len(tmp):
        ct = tmp

print(ct)
print(f'\n\n\n\npt : {pt}')
ENC_BLOCK = xor(pt, ct)

forged_ct = xor(ENC_BLOCK, b'_F')[:2]
print(send(forged_ct))
