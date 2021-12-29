#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "player.h"

int main() {
    srand(time(0));
    //players = calloc(NUM_OF_PROSPECTS, sizeof(Player));
    for(int i = 0; i < PLAYER_CAPACITY; i++){
        generate_player();
    }
    return 0;
}
