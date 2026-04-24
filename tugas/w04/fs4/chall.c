#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void setup(void) {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(void) {
    char buf[64];

    setup();
    printf("Gift for you: %p\n", &system);
    do {
        fgets(buf, sizeof(buf), stdin);
        printf(buf);
    } while (strncmp(buf, "quit", 4) != 0);
    return 0;
}