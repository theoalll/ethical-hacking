from pwn import *

context.binary = './chall'
p = process('./chall')

payload = cyclic(200)
p.sendline(payload)

p.wait()
core = p.corefile

fault = core.fault_addr
print("fault:", hex(fault))

offset = cyclic_find(fault)
print("offset:", offset)