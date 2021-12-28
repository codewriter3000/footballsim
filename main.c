#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "player.h"

#define NUM_OF_PROSPECTS 500

// A utility function to print an array of size n
void printArray(int arr[], int n)
{
    int i;
    for (i = 0; i < n; i++)
        printf("%d, ", arr[i]);
}

int main() {
    srand(time(0));
    int *ovrs = calloc(NUM_OF_PROSPECTS, sizeof(int));
    for(int i = 0; i < NUM_OF_PROSPECTS; i++){
        ovrs[i] = fetch_overall();
    }
    printf("\n");
    printArray(ovrs, NUM_OF_PROSPECTS);
    return 0;
}
