#include <stdio.h>
#include <stdlib.h>

struct book {
    char title[16];
    long page;
};

struct book *bookshelf[50];

void win() {
    system("/bin/sh");
}

void addBook() {
    int location;
    printf("Where do you want to put it?: ");
    scanf("%d%*c", &location);
    bookshelf[location] = malloc(sizeof(struct book));
    printf("Title: ");
    scanf("%15[^\n]s", bookshelf[location]->title);
    printf("Page: ");
    scanf("%ld%*c", &(bookshelf[location]->page));
}

void readBook() {
    int location;
    printf("Where is the book?: ");
    scanf("%d%*c", &location);
    printf("Title: %s\n", bookshelf[location]->title);
    printf("Page: %ld\n", bookshelf[location]->page);
}

void removeBook() {
    int location;
    printf("Where is the book?: ");
    scanf("%d%*c", &location);
    free(bookshelf[location]);
}

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

void greetings() {
    puts("Keep your books tidy with our bookshelf.");
}

int menu() {
    puts("\nMenu:");
    puts("1. Add a book to shelf");
    puts("2. Read a book from shelf");
    puts("3. Remove book from shelf");
    puts("4. Exit");
    printf("> ");
    
    int choice;
    scanf("%d%*c", &choice);
    return choice;
}

int main(int argc, char const *argv[]) {
    init();
    greetings();
    
    while (1) {
        int choice = menu();
        if (choice == 1) {
            addBook();
        }
        if (choice == 2) {
            readBook();
        }
        if (choice == 3) {
            removeBook();
        }
        if (choice == 4) {
            puts("Bye.");
            exit(0);
        }
    }
}
