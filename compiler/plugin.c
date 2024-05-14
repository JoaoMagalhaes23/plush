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

void print_int_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void print_2d_int_array(int **arr, int rows, int cols) {
    // Iterate through each row
    for (int i = 0; i < rows; i++) {
        // Iterate through each column in the current row
        for (int j = 0; j < cols; j++) {
            // Print the current element followed by a space
            printf("%d ", arr[i][j]);
        }
        // Print a newline character after each row
        printf("\n");
    }
}