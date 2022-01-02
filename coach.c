#include <stdlib.h>
#include "coach.h"

float generate_lean(){
    float r = (float)(rand()) / (float)RAND_MAX;
    return r;
}

void generate_coach(Team *team){
    Coach coach = {
            fetch_first_name(),
            fetch_last_name(),
            rand() % 49 + 50,
            generate_lean()
    };

    team->coach = coach;
}