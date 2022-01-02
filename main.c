#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "draft.h"
#include "game.h"
#include "csv_parser.h"

void draft(){
    if(PLAYER_CAPACITY < TEAM_CAPACITY * ROSTER_CAPACITY){
        printf("ERROR: PLAYER_CAPACITY < TEAM_CAPACITY * ROSTER_CAPACITY\n");
        exit(60);
    }

    // wipe the output text files clean
    FILE *fp = fopen("../data/output/prospects", "w");
    if(fp == NULL){
        printf("prospects not found");
        exit(65);
    }
    fwrite(fp, 0, 0, "");
    fclose(fp);

    // clearing players
    clear_players();

    // generate players
    printf("Generating Players:\n");
    for(int i = 0; i < PLAYER_CAPACITY; i++){
        generate_player();
    }

    // clearing teams
    clear_teams();

    // generate teams
    printf("\nGenerating Teams:\n");
    for(int i = 0; i < TEAM_CAPACITY; i++){
        generate_team();
    }

    // start draft
    printf("\nGenerating Draft:\n");
    start_draft();

    // wipe teamdata
    fp = fopen("../data/output/teamdata", "w");
    if(fp == NULL){
        printf("teamdata not found");
        exit(65);
    }
    fwrite(fp, 0, 0, "");
    fclose(fp);

    printf("writing to team data\n");
    // write to teamdata
    fp = fopen("../data/output/teamdata", "a+");
    if(fp == NULL){
        printf("teamdata not found");
        exit(65);
    }
    for(int i = 0; i < TEAM_CAPACITY; i++){
        write_team(fp, &teams[i]);
    }
    fclose(fp);
}

void play(){
    parse_teams();
    for(int i = 0; i < TEAM_CAPACITY; i++){
        printf("%d) %s: %2.1f (%2.1f OFF, %2.1f DEF)\n",
               i+1,
               get_team_name(&teams[i]),
               average_ovr(&teams[i]),
               average_ovr_offense(&teams[i]),
               average_ovr_defense(&teams[i]));
    }
    int home_team, away_team;
    printf("Select the home team you want to play...\n");
    scanf("%d", &home_team);
    printf("Select the away team you want to play...\n");
    scanf("%d", &away_team);
    play_game(&teams[home_team-1], &teams[away_team-1]);
}

int main() {
    srand(time(0));
    while(true){
        printf("Select an option:\n");
        printf("1) Draft a league\n");
        printf("2) Play a game\n");
        printf("3) Exit\n");
        char option;
        scanf("%c", &option);
        switch(option){
            case '1':
                draft();
                break;
            case '2':
                play();
                break;
            case '3':
                return 0;
            case '\n':
                break;
            default:
                printf("You entered %c\n", option);
                printf("Type 1, 2, or 3 to select one of the options\n");
        }
    }
}
