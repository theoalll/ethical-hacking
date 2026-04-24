from pwn import *

IP, PORT = '152.118.201.241', 3003

context.log_level = 'debug'

p = remote(IP, PORT)

try:
    while True:
        data = p.recvuntil(b'"', drop=True)
        askedString = p.recvuntil(b'"', drop=True)
        
        p.sendline(askedString)

        response = p.recvline()
        if b"CSCE" in response:
            print("\n[!] Flag ditemukan!")
            print(response.decode())
            break
except EOFError:
    print("\n[!] Koneksi ditutup oleh server.")
except Exception as e:
    print(f"Terjadi kesalahan: {e}")

p.close()