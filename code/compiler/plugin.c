#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void print_int(int value) {
    printf("%d", value);
}

void print_string(const char* value) {
    printf("%s", value);
}

void print_boolean(int llvm_i1) {
    if (llvm_i1) {
        printf("true");
    } else {
        printf("false");
    }
}

void print_float(float value) {
    printf("%f", value);
}

void print_int_array(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        printf("%d ", arr[i]);
    }
}

void print_2d_int_array(int **arr, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", arr[i][j]);
        }
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
    char buffer[12];

    sprintf(buffer, "%d", num);

    char* result = malloc(strlen(buffer) + 1);

    if (result == NULL) {
        return NULL;
    }

    strcpy(result, buffer);

    return result;
}