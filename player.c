#include "player.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>

void generate_player(){
    Player tmp = { .first_name = fetch_first_name(),
                   .last_name = fetch_last_name(),
                   .overall = fetch_overall() };
    players[sizeof players] = tmp;
}

char *fetch_first_name(){
    char *tmp;
    if(sizeof players == 0){
        first_names = fopen("../data/first_names", "r");
    }
    srand(time(0));
    int r = rand() % 1218;
    fgets(tmp, r, first_names);
    return tmp;
}

char *fetch_last_name(){
    char *tmp;
    if(sizeof players == 0){
        last_names = fopen("../data/last_names", "r");
    }
    srand(time(0));
    int r = rand() % 8000; //88798;
    fgets(tmp, r, last_names);
    return tmp;
}

//// Spaghetti code that worked in a previous attempt of this project
//
//static int next_value(int x, int l, int i){ //x = 0, l = random number, i = 0
//    int j = 88*exp(-1*pow(x-63, 2)/(2*pow(15, 2)));
//    if(i+j >= l){
//        return x;
//    } else {
//        return next_value(x+1, l+1, i+j);
//    }
//}
//
//// between 0 and 3138
//static int generate_overall(int n){;
//    return next_value(0, n, 0);
//}
//
//// End spaghetti code

double bell_curve(int x){
    double top = 0;
    for(int i = 0; i < 1024; i++){
        double val = 50 + 50.0*i/1024;
        top += pow(val - 75, 2);
    }
    double stddev = sqrt(top/1024);
    return 173/(stddev*sqrt(2*M_PI)) * exp(-0.5*pow((x-75)/stddev, 2));
    //return 900*amp/(stddev*sqrt(2*M_PI))* exp(-1/1.01*pow(top/stddev, 2));
}

static int a = 1;

int fetch_overall(){
    int raw_ovr = 0;
    int threshold = rand() % 130 + 1; // 194 if amp is 1
    //printf("%d, ", threshold);

    for(int ovr = 50; ovr < 99; ovr++){
        raw_ovr += bell_curve(ovr);
        if(raw_ovr > threshold){
            return ovr;
        }
    }

    printf("How the fuck did I get here? %d\n", threshold);
    return -1;
}