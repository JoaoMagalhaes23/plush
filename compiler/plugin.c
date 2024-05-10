#include <stdio.h>

void print_int(int value) {
    printf("%d\n", value);
}

void print_string(const char* value) {
    printf("%s\n", value);
}

void print_boolean(int llvm_i1) {
    if (llvm_i1) {
        printf("true\n");
    } else {
        printf("false\n");
    }
}
