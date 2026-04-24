#include <stdio.h>
#include <stdlib.h>

#define EMP_NAME_LEN 0x10
#define ENDORSEMENT_LEN 0x18

typedef struct employee {
    void (*print_func)(struct employee *);
    char name[EMP_NAME_LEN];
} employee_t;

employee_t *g_employee = NULL;
char *endorsement = NULL;

void win(void) {
    system("/bin/sh");
}

void print_employee(employee_t *emp) {
    printf("Employee name: %s\n", emp->name);
}

void create_employee(void) {
    if (g_employee != NULL) {
        puts("Employee already created.");
        return;
    }

    g_employee = malloc(sizeof(employee_t));
    g_employee->print_func = print_employee;
    
    printf("Name: ");
    fgets(g_employee->name, EMP_NAME_LEN, stdin);

    puts("Employee created.");
}

void view_employee(void) {
    if (g_employee == NULL) {
        puts("No employee available.");
        return;
    }
    (g_employee->print_func)(g_employee);
}

void delete_employee(void) {
    if (g_employee == NULL) {
        puts("No employee available.");
        return;
    }
    free(g_employee);
    puts("Employee deleted.");
}

void endorse_employee(void) {
    endorsement = malloc(ENDORSEMENT_LEN);
    printf("Endorsement: ");
    fgets(endorsement, ENDORSEMENT_LEN, stdin);
    puts("Employee endorsed.");
}

void setup(void) {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void print_menu(void) {
    puts("=== Employee Management System ===");
    puts("1. Create Employee");
    puts("2. View Employee");
    puts("3. Delete Employee");
    puts("4. Endorse Employee");
    printf(">> ");
}

int get_choice(void) {
    char buf[16];
    fgets(buf, sizeof(buf), stdin);
    return atoi(buf);
}

int main(void) {
    setup();
    while (1) {
        print_menu();
        int choice = get_choice();
        switch (choice) {
            case 1:
                create_employee();
                break;
            case 2:
                view_employee();
                break;
            case 3:
                delete_employee();
                break;
            case 4:
                endorse_employee();
                break;
            default:
                puts("Invalid choice.");
                break;
        }
    }
    return 0;
}