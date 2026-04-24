#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define VERY_SMALL 32
#define NOT_SMALL 64

void debug_function() {
    printf("ENTERING SECRET FUNCTION\n");
    system("/bin/sh");
}

int bad_code() {
    char small_buffer[VERY_SMALL] = {0};
    int n = read(0, small_buffer, NOT_SMALL);
    return n;
}

int main() {
    bad_code();
    printf("You're back! Hooray!");
    return 0;
}