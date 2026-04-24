#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#define NOTE_CONTENT_LEN 0x100

typedef struct note {
    char content[NOTE_CONTENT_LEN];
    void (*operation_func)(struct note *);
} note_t;

note_t *g_note;

void win(char *cmd) {
    system(cmd);
}

int get_int(void) {
    char buf[0x10];
    fgets(buf, sizeof(buf), stdin);
    return atoi(buf);
}

void print_note(note_t *note) {
    printf("Note content: %s\n", note->content);
}

void clear_note(note_t *note) {
    memset(note, NOTE_CONTENT_LEN, 0);
}

void edit_note(note_t *note) {
    printf("Enter new content length: ");
    int new_len = get_int();
    if (new_len <= 0) {
        puts("Invalid length.");
        return;
    }
    printf("New content: ");
    read(0, g_note->content, new_len);
}

void print_menu(void) {
    puts("1. Print Note");
    puts("2. Clear Note");
    puts("3. Edit Note");
    printf(">> ");
}

void setup(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    g_note = malloc(sizeof(note_t));
}

int main(void) {
    setup();
    while (1) {
        print_menu();
        int choice = get_int();
        switch (choice) {
            case 1:
                g_note->operation_func = print_note;
                break;
            case 2:
                g_note->operation_func = clear_note;
                break;
            case 3:
                g_note->operation_func = edit_note;
                break;
            default:
                puts("Invalid choice.");
                break;
        }
        if (g_note->operation_func) {
            (g_note->operation_func)(g_note);
        }
    }
    return 0;
}