#include <stdio.h>
#include <stdlib.h>

FILE* fp;
char flag[200];

void target(int p1, int p2, int p3) {
    if (p1 == 0x12345678 && p2 == 0x87654321 && p3 == 0xabcdef01) {
        puts("flag opened.");
        fp = fopen("flag.txt","r");
    } else if (p1 == 0x1337c0de && p2 == 0x1337c4f3) {
        puts("flag read.");
        fgets(flag, 100, fp);
    } else if (p1 == 0xf4d4f4d4) {
        puts(flag);
    }
}

void vuln() {
    char buf[69];
    puts("good luck!");
    gets(buf);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    vuln();
    return 0;
}
