#include <stdio.h>
#include <stdlib.h>

int main(int argc, char const *argv[]) {
	setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
	int *hack_me = malloc(10);
	*hack_me = 5;
	char buf[16];

	puts("Are you ready kids?");
	scanf("%15s", buf);

	printf("Your input: ");
	printf(buf);
	printf("\n");

	if(*hack_me == 1337)
		system("echo \"Hi, here is your flag\"; cat flag.txt");
	else
		puts("Ok thanks");
	return 0;
}
