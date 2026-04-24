from pwn import *

binary = "./baby-shellcode"
elf = ELF(binary)
elf.checksec()
