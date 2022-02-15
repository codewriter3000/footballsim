#ifndef __LEAGUE_H
#define __LEAGUE_H

typedef struct {
    char* Team;
    char* Schedule;
} League;

void league();

void generate_league();

#endif