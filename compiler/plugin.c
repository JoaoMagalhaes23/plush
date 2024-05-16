#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

void print_float(float value) {
    printf("%f\n", value);
}

void print_int_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
    printf("\n");
}

void print_2d_int_array(int **arr, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }
}


char* concatenate_strings(const char* str1, const char* str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);

    char* result = (char*)malloc(len1 + len2 + 1);
    if (result == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(EXIT_FAILURE);
    }

    strcpy(result, str1);

    strcat(result, str2);

    return result;
}

char* int_to_string(int num) {
    // Buffer to hold the string representation of the integer
    // Adjust the size if you expect larger integers
    char buffer[12]; // Enough to hold an integer including the sign and null terminator

    // Convert the integer to a string
    sprintf(buffer, "%d", num);

    // Allocate memory for the result string
    char* result = malloc(strlen(buffer) + 1);

    // Check if the memory allocation was successful
    if (result == NULL) {
        return NULL; // Memory allocation failed
    }

    // Copy the string to the allocated memory
    strcpy(result, buffer);

    // Return the result
    return result;
}