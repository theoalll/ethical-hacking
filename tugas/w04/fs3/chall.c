#include <stdio.h>
#include <stdlib.h>

void read_flag(char *buf, size_t len) {
    FILE *fp = fopen("flag.txt", "r");
    if (!fp) {
        perror("fopen");
        exit(1);
    }
    fgets(buf, len, fp);
    fclose(fp);
}

int main(void) {
    char flag[64];
    char buf[64];

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    read_flag(flag, sizeof(flag));

    printf("Name: ");
    fgets(buf, sizeof(buf), stdin);
    printf("Hello ");
    printf(buf);

    return 0;
}