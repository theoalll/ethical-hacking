from pwn import *

io = remote('152.118.201.241', 3025)

def add(idx, title, page):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'?: ', str(idx).encode())
    io.sendlineafter(b'Title: ', title)
    io.sendlineafter(b'Page: ', str(page).encode())

for i in [0, 50, 100, 200, 500]:
    print(f"Testing index {i}")
    add(i, b'A', 1)

print("Done")
io.close()
