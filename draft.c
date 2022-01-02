#include "draft.h"
#include <stdio.h>
#include <stdlib.h>

Player free_agents[PLAYER_CAPACITY] = { 0 };

void start_draft(){
    // copy contents of players into prospects
    for(int i = 0; i < num_of_players; i++){
        free_agents[i] = players[i];
    }

//    // assign user team
//    int user_team_index = rand() % (TEAM_CAPACITY - 1);
//    Team *user_team = &teams[user_team_index];
//    printf("Your team is the %s %s\n",
//           user_team->city,
//           user_team->mascot);

    // start snake draft
    for(int i = 0; i < ROSTER_CAPACITY; i++){
        printf("Round %d:\n", i + 1);
        if((i+1) % 2 == 1){
            for(int j = 0; j < TEAM_CAPACITY; j++){
                Player pick = AI_pick();
                printf("The %s %s select %s %s (%s): %d ovr\n",
                       teams[j].city,
                       teams[j].mascot,
                       pick.first_name,
                       pick.last_name,
                       get_position(&pick, true),
                       pick.overall);
                teams[j].roster[i] = pick;
            }
        } else {
            for(int j = TEAM_CAPACITY-1; j >= 0; j--){
                Player pick = AI_pick();
                printf("The %s %s select %s %s (%s): %d ovr\n",
                       teams[j].city,
                       teams[j].mascot,
                       pick.first_name,
                       pick.last_name,
                       get_position(&pick, true),
                       pick.overall);
                teams[j].roster[i] = pick;
            }
        }
    }
}

Player AI_pick(){
    for(int i = 99; i > 49; i--){
        for(int j = 0; j < num_of_players; j++){
            if(free_agents[j].overall == i){
                Player pick = free_agents[j];
                free_agents[j].overall = -1;
                return pick;
            }
        }
    }
}