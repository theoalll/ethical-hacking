#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

__attribute__((naked, used))
void hi(void) {
    __asm__("pop %rdi; ret");
}

__attribute__((naked, used))
void hey(void) {
    __asm__("pop %rsi; pop %r15; ret");
}

void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void win() {
    char flag[64];
    FILE *f = fopen("flag.txt","r");
    fgets(flag,64,f);
    puts(flag);
}

void vuln() {
    char buf[64];;
    int pivot_size = rand() % 100;
    char pivot[pivot_size]; 

    printf("pivot @ %p\n", pivot);
    printf("win @ %p\n", &win);
    
    do {
        fgets(buf, sizeof(buf), stdin);
        printf(buf);
    } while (strncmp(buf, "quit", 4) != 0);

}

int main(void) {
    setup();
    vuln();
    return 0;
}