#include <stdio.h>
#include <stdlib.h>

char *binsh = "/bin/sh";

void vuln() {
    char buf[69];
    gets(buf);
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    printf("string /bin/sh: %p\n", binsh);
    printf("puts: %p\n", puts);
    vuln();
    return 0;
}
