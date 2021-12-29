#include <bits/types/FILE.h>
#include "player.h"

#define TEAM_CAPACITY 32
#define CITY_RARITY 0.1

typedef struct {
    char *city, *mascot;
    Player *roster;
} Team;

extern Team teams[TEAM_CAPACITY];
extern int num_of_teams;
void generate_team();

char *fetch_city();
char *fetch_mascot();

void print_team(Team*);