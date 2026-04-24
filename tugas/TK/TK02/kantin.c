#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void clear_environment() {
    clearenv();
}

void banner() {
    puts("=== Kantin Overflow: Mie Ayam Edition ===");
    puts("Selamat datang di kantin pacil!");
    puts("Menu favorit hari ini:");
    puts("- Mie Ayam Original");
    puts("- Mie Ayam Bakso");
    puts("- Mie Ayam Spesial (rahasia...)");
    puts("");
}

void kasir() {
    char order[64];

    puts("Masukkan pesanan kamu:");
    printf("(nomor meja kamu: %p)\n", order);
    printf("> ");

    ssize_t n = read(0, order, 256);

    if (n <= 0) {
        puts("Input error.");
        exit(1);
    }

    // filter forbidden bytes
    for (int i = 0; i < n; i++) {
        if (order[i] == '\x0a') {
            puts("Eh jangan aneh-aneh dong inputnya!");
            exit(1);
        }
    }

    order[n] = '\0';

    puts("\nPesanan diterima!");
    printf("Kamu pesan: %s\n", order);

    puts("\nHmm... katanya ada resep rahasia di dapur...");
    puts("Tapi cuma orang spesial yang bisa lihat file itu...");
}

int main() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    clear_environment();
    banner();
    kasir();

    puts("\nTerima kasih sudah makan di kantin!");
    return 0;
}