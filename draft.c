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
                Player pick = AI_pick(teams[j].off_players, teams[j].def_players, teams[j].coach.lean);
                printf("The %s %s select %s %s (%s): %d ovr\n",
                       teams[j].city,
                       teams[j].mascot,
                       pick.first_name,
                       pick.last_name,
                       get_position(&pick, true),
                       pick.overall);
                teams[j].roster[i] = pick;
                if(get_position(&pick, false)[0] == 'O'){
                    teams[j].off_players++;
                } else if(get_position(&pick, false)[0] == 'D'){
                    teams[j].def_players++;
                } else {
                    // get_position has a different value than what you anticipate
                    exit(420);
                }
            }
        } else {
            for(int j = 0; j < TEAM_CAPACITY; j++){
                Player pick = AI_pick(teams[j].off_players, teams[j].def_players, teams[j].coach.lean);
                printf("The %s %s select %s %s (%s): %d ovr\n",
                       teams[j].city,
                       teams[j].mascot,
                       pick.first_name,
                       pick.last_name,
                       get_position(&pick, true),
                       pick.overall);
                teams[j].roster[i] = pick;
                if(get_position(&pick, false)[0] == 'O'){
                    teams[j].off_players++;
                } else if(get_position(&pick, false)[0] == 'D'){
                    teams[j].def_players++;
                } else {
                    // get_position has a different value than what you anticipate
                    exit(420);
                }
            }
        }
    }
}

Player AI_pick(int off_players, int def_players, double lean){
    for(int i = 99; i > 49; i--){
        for(int j = 0; j < num_of_players; j++){
            // decide on offense or defense
            // first 10 picks are wherever you weigh
            double r = (double)(rand()) / (double)RAND_MAX;
            if(off_players + def_players <= 10 && r > lean){
                if(free_agents[j].overall == i && free_agents[j].is_offense == false){
                    Player pick = free_agents[j];
                    free_agents[j].overall = -1;
                    return pick;
                }
            } else if(off_players + def_players <= 10 && r < lean){
                if(free_agents[j].overall == i && free_agents[j].is_offense == true){
                    Player pick = free_agents[j];
                    free_agents[j].overall = -1;
                    return pick;
                }
            } else {
                if(free_agents[j].overall == i){
                    Player pick = free_agents[j];
                    free_agents[j].overall = -1;
                    return pick;
                }
            }
        }
    }
}