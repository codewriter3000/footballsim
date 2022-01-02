#include <stdlib.h>
#include <stdio.h>
#include "team.h"
#include "game.h"

#define OVR_DIFF_MULTIPLIER 0.03

Team play_game(Team *home_team, Team *away_team){
    int home_pts = 0, away_pts = 0;
    double ovr_diff_home = average_ovr_offense(home_team) - average_ovr_defense(away_team);
    double ovr_diff_away = average_ovr_offense(away_team) - average_ovr_defense(home_team);
    //printf("ovr_diff_home: %f\n", ovr_diff_home);
    //printf("ovr_diff_away: %f\n", ovr_diff_away);
    for(int i = 0; i < 12; i++){
        printf("\n");
        home_pts += drive(home_team, i%2 == 0 ? ovr_diff_home : -ovr_diff_home);
        away_pts += drive(away_team, i%2 == 0 ? ovr_diff_away : -ovr_diff_away);
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

double multiplier(double x){
    return OVR_DIFF_MULTIPLIER*x + 1 < 0.72 ? 0.72 : OVR_DIFF_MULTIPLIER*x + 1;
}

int drive(Team *team, double ovr_diff){
    char *team_name = get_team_name(team);
    double r = (double)(rand()) / (double)RAND_MAX;
    r *= multiplier(ovr_diff);
    if(r <= 0.3511) {
        // 17.92% = turnover
        printf("The %s just turned the ball over\n", team_name);
        return 0;
    } else if(r <= 0.5303){
        // 35.11% = punt
        printf("The %s are punting\n", team_name);
        return 0;
    } else if(r <= 0.7193){
        // 18.9% = field goal
        printf("The %s kicked a successful field goal\n", team_name);
        return 3;
    } else {
        // 28.07% = touchdown
        printf("TOUCHDOWN %s\n", team_name);
        return PAT();
    }
}

int PAT(){
    double r = (double)(rand()) / (double)RAND_MAX;
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