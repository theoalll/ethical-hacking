#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_CHUNKS 10
#define MENU "\nMenu:\n1. Add\n2. Show\n3. Delete\n4. Edit\n5. Exit\nChoice: "

void *chunks[MAX_CHUNKS];
size_t chunk_sizes[MAX_CHUNKS];

void win() {
    system("sh");
}

int read_int() {
    char buf[16];
    read(0, buf, sizeof(buf));
    return atoi(buf);
}

void add() {
    int idx;
    size_t size;
    
    printf("Enter idx: ");
    idx = read_int();
    
    if (idx < 0 || idx >= MAX_CHUNKS) {
        printf("Invalid index!\n");
        return;
    }
    
    if (chunks[idx] != NULL) {
        printf("Chunk already exists at this index!\n");
        return;
    }
    
    printf("Enter size: ");
    scanf("%zu", &size);
    
    if (size < 0x410 || size > 0x1000) {
        printf("Invalid size!\n");
        return;
    }
    
    chunks[idx] = malloc(size);
    chunk_sizes[idx] = size + 8;
}

void edit() {
    int idx;
    
    printf("Enter idx: ");
    idx = read_int();
    
    if (idx < 0 || idx >= MAX_CHUNKS || chunks[idx] == NULL) {
        printf("Invalid index or chunk doesn't exist!\n");
        return;
    }
    
    printf("Enter content: ");
    ssize_t n = read(0, chunks[idx], chunk_sizes[idx]);
    ((char *)chunks[idx])[n] = '\0';
    
    printf("Chunk edited\n");
}

void show() {
    int idx;
    
    printf("Enter idx: ");
    idx = read_int();
    
    if (idx < 0 || idx >= MAX_CHUNKS || chunks[idx] == NULL) {
        printf("Invalid index or chunk doesn't exist!\n");
        return;
    }
    
    printf("Content: %s\n", (char*)chunks[idx]);
}

void delete() {
    int idx;
    
    printf("Enter idx: ");
    idx = read_int();
    
    if (idx < 0 || idx >= MAX_CHUNKS || chunks[idx] == NULL) {
        printf("Invalid index or chunk doesn't exist!\n");
        return;
    }
    
    free(chunks[idx]);
    chunks[idx] = NULL;
    chunk_sizes[idx] = 0;
    printf("Chunk deleted\n");
}

int main() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    int choice;
    
    while (1) {
        printf(MENU);
        choice = read_int();
        
        switch (choice) {
            case 1:
                add();
                break;
            case 2:
                show();
                break;
            case 3:
                delete();
                break;
            case 4:
                edit();
                break;
            case 5:
                exit(0);
                break;
            default:
                printf("Invalid choice!\n");
                break;
        }
    }
    
    return 0;
}