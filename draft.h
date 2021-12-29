#ifndef _DRAFT__H
#define _DRAFT__H

#include "team.h"

#define ROSTER_CAPACITY 53

extern Player free_agents[PLAYER_CAPACITY];

void start_draft();

Player AI_pick();

#endif