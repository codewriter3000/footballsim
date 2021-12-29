#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "draft.h"

int main() {
    srand(time(0));

    if(PLAYER_CAPACITY < TEAM_CAPACITY * ROSTER_CAPACITY){
        printf("ERROR: PLAYER_CAPACITY < TEAM_CAPACITY * ROSTER_CAPACITY\n");
        exit(60);
    }

    // wipe the output text files clean
    FILE *fp = fopen("../data/output/prospects", "w");
    fwrite(fp, 0, 0, "");
    fclose(fp);

    // generate players
    printf("Players:\n");
    for(int i = 0; i < PLAYER_CAPACITY; i++){
        generate_player();
    }

    // generate teams
    printf("\nTeams:\n");
    for(int i = 0; i < TEAM_CAPACITY; i++){
        generate_team();
    }

    // start draft
    printf("\nDraft:\n");
    start_draft();
    return 0;
}
