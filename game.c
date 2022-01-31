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
//        printf("Home team coach ovr: %d\n", home_team->coach.overall);
//        printf("Away team coach ovr: %d\n", away_team->coach.overall);
        home_pts += drive(home_team, ovr_diff_home);
        away_pts += drive(away_team, ovr_diff_away);
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

double multiplier(double plr, double coach){
    double player_modifier = OVR_DIFF_MULTIPLIER*plr + 1;
//    printf("player modifier: %f\n", player_modifier);
//    printf("coach modifier: %f\n", (1.2+coach)/85);
    double coach_modifier = player_modifier * ((1.2+coach)/85);
//    printf("total modifier: %f\n", coach_modifier < 0.72 ? 0.72 : coach_modifier);
    return coach_modifier < 0.72 ? 0.72 : coach_modifier;
}

int drive(Team *team, double ovr_diff){
    char *team_name = get_team_name(team);
    double r = (double)(rand()) / (double)RAND_MAX;
//    printf("Coach ovr: %d\n", team->coach.overall);
    r *= multiplier(ovr_diff, team->coach.overall);
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