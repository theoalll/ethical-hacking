#include<stdio.h>
#include<stdlib.h>

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
}

struct item {
    long int price;
    char *name;
};

int N = 20;
int idx = 0;
struct item *items[20];
long itemSelled = 0;
long targetSell = 0x1234567812345678;

void addItem() {
    if (idx == N) {
        puts("Our shop is full.");
        return;
    }

    items[idx] = malloc(sizeof(struct item));
    items[idx]->name = malloc(0x69);
    
    printf("Item name: ");
    scanf(" %[^\n]", items[idx]->name);

    printf("Item price: ");
    scanf("%ld", &(items[idx]->price));

    idx++;
    puts("Item added successfully.");
}

void editItem() {
    if (idx == 0) {
        puts("Our shop is empty.");
        return;
    }
    printf("Item index (0 - %d): ", idx - 1);

    int editedIdx;
    scanf("%d", &editedIdx);
    if (editedIdx < 0 || editedIdx >= idx) {
        puts("Item index not found.");
        return;
    }

    printf("Item name: ");
    scanf(" %[^\n]", items[editedIdx]->name);

    printf("Item price: ");
    scanf("%ld", &(items[editedIdx]->price));

    puts("Item edited successfully.");
}

void listItem() {
    puts("\n===========================================");
    puts("Item List");
    for (int i = 0; i < idx; i++) {
        printf("Name: %s\n", items[i]->name);
        printf("Price: %ld\n", items[i]->price);
        puts("");
    }
    puts("===========================================\n");
}

int menu() {
    puts("Menu:");
    puts("1. Add item");
    puts("2. Edit item");
    puts("3. List of added items");
    puts("4. Sell item");
    puts("5. Get flag");
    puts("6. Exit");
    printf("> ");
    
	int choice;
    scanf("%d", &choice);
	return choice;
}


void sellItem() {
    puts("Oops, I don't give you access to sell yet.");
}

void getFlag() {
    if (itemSelled != targetSell) {
        puts("You don't achieve the target yet. Try to sell some items first.");
        return;
    }
	system("cat flag.txt");
}

void greetings() {
    puts("Welcome to our shop :D");
    puts("You are our new manager.");
    puts("Your job now is to fill our shop with new items and sell it.");
    puts("For now, you can add up to 20 items in your list.");
    puts("I will give you flag if you do your job correctly.");
    puts("Good luck.");
}

int main() {
    init();
    greetings();
    
    while (1) {
        int choice = menu();
        if (choice == 1) {
            addItem();
        }
        if (choice == 2) {
            editItem();
        }
        if (choice == 3) {
            listItem();
        }
        if (choice == 4) {
            sellItem();
        }
        if (choice == 5) {
            getFlag();
        }
        if (choice == 6) {
            puts("Bye.");
            exit(0);
        }
    }
}
