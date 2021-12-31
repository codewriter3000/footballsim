#include <stdlib.h>
#include <stdio.h>
#include "team.h"
#include "game.h"

Team play_game(Team *home_team, Team *away_team){
    int home_pts = 0, away_pts = 0;
    double ovr_diff = average_ovr(home_team) - average_ovr(away_team);
    for(int i = 0; i < 12; i++){
        printf("\n");
        home_pts += drive(home_team, ovr_diff);
        away_pts += drive(away_team, -ovr_diff);
        if(i != 0)  printf("----Score: %d - %d----\n", home_pts, away_pts);
        printf("Press any key to start the next drive");
        char k;
        scanf("%c", &k);
    }
    printf("----FINAL SCORE: %d - %d----\n", home_pts, away_pts);
    if(home_pts > away_pts){
        printf("The %s won the game\n", get_team_name(home_team));
    } else if(away_pts > home_pts){
        printf("The %s won the game\n", get_team_name(away_team));
    } else {
        printf("The %s and the %s have tied\n",
               get_team_name(home_team),
               get_team_name(away_team));
    }
}

int drive(Team *team, double ovr_diff){
    char *team_name = get_team_name(team);
    float r = (float)(rand()) / (float)RAND_MAX;
    if(r <= 0.3511){
        // 35.11% = punt
        printf("The %s are punting\n", team_name);
        return 0;
    } else if(r <= 0.6318){
        // 28.07% = touchdown
        printf("TOUCHDOWN %s\n", team_name);
        return PAT();
    } else if(r <= 0.8208){
        // 18.9% = field goal
        printf("The %s kicked a successful field goal\n", team_name);
        return 3;
    } else {
        // turnover
        printf("The %s just turned the ball over\n", team_name);
        return 0;
    }
}

int PAT(){
    int r = rand();
    if(r <= 0.95){
        printf("The extra point is good\n");
        return 7;
    } else if(r <= 0.975){
        printf("The extra point is no good\n");
        return 6;
    } else {
        printf("The 2-point conversion is good\n");
        return 8;
    }
}