#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
    char buf[128];
    int n = 10;

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    printf("Address: %p\n", &n);
    puts("Enter your shellcode:");
    gets(buf);
    puts("Thanks! Executing now...");

    puts("Finishing Executing Shellcode. Exiting now...");
    return 0;
}
