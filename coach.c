#include <stdlib.h>
#include <stdio.h>
#include "coach.h"

float generate_lean(){
    float r = (float)(rand()) / (float)RAND_MAX;
    return r;
}

Coach generate_coach(){
    Coach coach = {
            fetch_first_name(),
            fetch_last_name(),
            rand() % 49 + 50,
            generate_lean()
    };
    return coach;
}

void print_coach(Coach *coach){
    printf("%s %s, ovr: %d, lean: %f\n",
           coach->first_name,
           coach->last_name,
           coach->overall,
           coach->lean);
}