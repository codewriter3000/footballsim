#ifndef _COACH__H
#define _COACH__H

#include "player.h"

typedef struct {
    char *first_name, *last_name;
    int overall;
    float lean;
} Coach;

float generate_lean();

Coach generate_coach();

void print_coach(Coach*);

#endif