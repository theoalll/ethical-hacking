#include <stdio.h>
#include <stdlib.h>

void win() {
	char flag[64];
    FILE *f = fopen("flag.txt","r");
    fgets(flag,64,f);
	puts(flag);
}

int main(int argc, char const *argv[])
{
	setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
	int hack_me = 0x5;
	char buf[16];

	puts("What do you want?");
	gets(buf);
	puts("Noted.");
	return 0;
}
