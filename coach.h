#ifndef _COACH__H
#define _COACH__H

#include "team.h"
#include "player.h"

typedef struct {
    char *first_name, *last_name;
    int overall;
    float lean;
} Coach;

float generate_lean();

void generate_coach(Team *team);
int fetch_coaching_overall();

void print_coach(Coach*);

#endif