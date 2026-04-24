#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define TITLE_SIZE 16
#define BOOKMARK_SIZE 104

void win() {
    FILE *f = fopen("flag.txt","r");
    if (f == NULL) {
        puts("Error, please contact asdos.");
        exit(1);
    }
    char flag[100];
    fgets(flag, 100, f);
    puts(flag);
}

struct book {
    char title[TITLE_SIZE];
    char *bookmark;
    long page;
};

struct book *bookshelf[50];

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void addBook() {
    int location;
    printf("Where do you want to put it?: ");
    scanf("%d%*c", &location);
    
    if (location < 0 || location >= 50) {
        puts("Invalid shelf location!");
        return;
    }
    
    bookshelf[location] = malloc(sizeof(struct book));
    bookshelf[location]->bookmark = malloc(BOOKMARK_SIZE);
    
    printf("Bookmark note: ");
    scanf("%103[^\n]%*c", bookshelf[location]->bookmark);
    printf("Title: ");
    scanf("%15[^\n]%*c", bookshelf[location]->title);    
    printf("Page: ");
    scanf("%ld%*c", &(bookshelf[location]->page));
    puts("Book added successfully!");
}

void editBook() {
    int location;
    printf("Where is the book?: ");
    scanf("%d%*c", &location);
    
    if (location < 0 || location >= 50 || bookshelf[location] == NULL) {
        puts("No book at that location!");
        return;
    }

    printf("Somehow the bookmark is gone, but you can still edit the book!\n");
    printf("Title: ");
    scanf("%23[^\n]%*c", bookshelf[location]->title);
    printf("Page: ");
    scanf("%ld%*c", &(bookshelf[location]->page));
}

void removeBook() {
    int location;
    printf("Where is the book?: ");
    scanf("%d%*c", &location);
    
    if (location < 0 || location >= 50 || bookshelf[location] == NULL) {
        puts("No book at that location!");
        return;
    }
    
    if (bookshelf[location]->bookmark != NULL) {
        free(bookshelf[location]->bookmark);
        bookshelf[location]->bookmark = NULL;
    }
    
    free(bookshelf[location]);
    bookshelf[location] = NULL;
    puts("Book removed!");
}

int menu() {
    puts("\nMenu:");
    puts("1. Add a book to shelf");
    puts("2. Edit a book from shelf");
    puts("3. Remove book from shelf");
    puts("4. Exit");
    printf("> ");
    
    int choice;
    scanf("%d%*c", &choice);
    return choice;
}

void greetings() {
    puts("Keep your books tidy with our bookshelf.");
}

int main(int argc, char const *argv[]) {
    init();
    greetings();

    long good, luck;
    printf("Input some numbers: ");
    scanf("%ld%*c %ld%*c", &good, &luck);
    printf("Leaky leaky, its time for schoo: %p UwU %p\n", &win, &good);
    
    while (1) {
        int choice = menu();
        if (choice == 1) {
            addBook();
        } else if (choice == 2) {
            editBook();
        } else if (choice == 3) {
            removeBook();
        } else if (choice == 4) {
            puts("Goodbye!");
            break;
        } else {
            puts("Invalid choice!");
        }
    }
}