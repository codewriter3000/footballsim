#include <bits/types/FILE.h>
#include <stdbool.h>
#include "player.h"

#ifndef _TEAM__H
#define _TEAM__H

#include "coach.h"

#define ROSTER_CAPACITY 53
#define TEAM_CAPACITY 32
#define CITY_RARITY 0.1

typedef struct {
    char *city, *mascot;
    Player roster[ROSTER_CAPACITY];
    Coach coach;
} Team;

extern Team teams[TEAM_CAPACITY];
extern int num_of_teams;
void clear_teams();
void generate_team();

char *fetch_city();
char *fetch_mascot();

void print_team(Team*);

void write_team(FILE*, Team*);
void write_coach(FILE*, Coach*);
void write_player(FILE*, Player*, bool);

char *get_team_name(Team*);
double average_ovr(Team*);

#endif