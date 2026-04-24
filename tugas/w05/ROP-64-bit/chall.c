#include <stdio.h>
#include <stdlib.h>

FILE* fp;
char flag[200];

void target(long p1, long p2) {
    if (p1 == 0xcafebabecafebabe && p2 == 0xdeadc0dedeadc0de) {
        puts("flag opened.");
        fp = fopen("flag.txt","r");
    } else if (p1 == 0x6767676767676767 && p2 == 0x1337beef1337beef) {
        puts("flag read.");
        fgets(flag, 100, fp);
    } else if (p1 == 0x4141414142424242 && p2 == 0x4343434344444444) {
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
