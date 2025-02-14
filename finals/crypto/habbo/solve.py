from pwn import remote

p = remote("localhost", 1234)

payloads = [
    # payload
    (b"AAAAAAAAAAAAA -1,             ",
    # block index to cut-paste for timestamp
    [0, 1, 2, 4, 3]),

    # payload
    (b"AAAAAAAAAAAAA\"               0,              :                          rand",
    # block index to override rand
    [3, 6, 5, 4]),

    # payload
    (b"AAAAAAAAAAAAA\"admin          : true}                        \"               ",
    # block index to cut paste for admin
    [3, 6, 4]),

    # payload
    (b'AAAAAAAAAAAAAAAAAAA',
    # block index to cut-paste for padding
    [-1])
]

crafted_token_block = []
for payload, index in payloads:
    p.sendline(b"1")
    p.sendline(payload)

    p.recvuntil(b"Here is your token: ")
    reference = p.recvline().strip()
    ref_block = [reference[i:i+32] for i in range(0, len(reference), 32)]

    for i in index:
        crafted_token_block.append(ref_block[i])

    p.sendline(b"3")

crafted_token = b"".join(crafted_token_block)
p.sendline(b"2")
p.sendline(crafted_token)
p.sendline(b"2")
p.recvuntil(b"FLAG: ")
flag = p.recvline().strip()
print(flag)