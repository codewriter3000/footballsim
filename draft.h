#ifndef _DRAFT__H
#define _DRAFT__H

#include "team.h"

extern Player free_agents[PLAYER_CAPACITY];

void start_draft();

Player AI_pick();

#endif