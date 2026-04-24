#include <stdio.h>
#include <stdlib.h>

void win() {
    char flag[64];
    FILE *f = fopen("flag.txt","r");
    fgets(flag,64,f);
    puts(flag);
}

int n;
long sum = 0;

int main(int argc, char const *argv[]) {
    char buf[16];
    long nums[4];
    
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    
    puts("How many times?");
    scanf("%d", &n);
    
    for (int i = 0; i < n; i++) {
        scanf("%ld%*c", &nums[i]);
        sum += nums[i];
    }
    printf("Result: %ld\n\n", sum);

    puts("Say something:");
    scanf("%s", buf);
    puts("Bye.");
}
