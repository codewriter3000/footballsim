#include "player.h"
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <math.h>
#include <stdbool.h>
#include <string.h>

void generate_player(){
    Player tmp = { .first_name = fetch_first_name(),
                   .last_name = fetch_last_name(),
                   .overall = fetch_overall() };
    print_player(&tmp);
    *(players + player_capacity++) = tmp;
}

char *fetch_first_name(){
    char *tmp = calloc(sizeof(char), 12);
    first_names = fopen("../data/first_names", "r");
    if(first_names == NULL){
        printf("first_names not found\n");
    }
    int r = rand() % (int)(1218 * FIRST_NAME_RARITY) + 1;
    char *line = calloc(13, sizeof(char));
    int l = 1, i = 0;
    char ch;
    do {
        ch = fgetc(first_names);
        if(ch == '\n') l++;
        else {
            if(l == r){
                line[i++] = ch;
            } else if(l > r){
                break;
            }
        }
    } while(ch != '\0');
    strcpy(tmp, line);
    fclose(first_names);
    return tmp;
}

char *fetch_last_name(){
    char *tmp = calloc(sizeof(char), 64);
    last_names = fopen("../data/last_names", "r");
    if(last_names == NULL){
        printf("last_names not found\n");
    }
    int r = rand() % (int)(88798 * LAST_NAME_RARITY) + 1;
    char *line = calloc(13, sizeof(char));
    int l = 1, i = 0;
    char ch;
    do {
        ch = fgetc(last_names);
        if(ch == '\n') l++;
        else {
            if(l == r){
                line[i++] = ch;
            } else if(l > r){
                break;
            }
        }
    } while(ch != '\0');
    strcpy(tmp, line);
    fclose(last_names);
    return tmp;
}

double bell_curve(int x){
    // standard deviation formula
    double top = 0;
    for(int i = 0; i < 1024; i++){ // summation
        double val = 50 + 50.0*i/1024;
        top += pow(val - 75, 2);
    }
    double stddev = sqrt(top/1024);

    // the bell curve function
    return 173/(stddev*sqrt(2*M_PI)) * exp(-0.5*pow((x-75)/stddev, 2));
}

int fetch_overall(){
    int raw_ovr = 0;
    int threshold = rand() % 130 + 1;

    for(int ovr = 50; ovr < 99; ovr++){
        raw_ovr += bell_curve(ovr);
        if(raw_ovr > threshold){
            return ovr;
        }
    }

    printf("How the fuck did I get here? %d\n", threshold);
    return -1;
}

void print_player(Player *player){
    printf("%s, %s, %d\n",
           player->first_name,
           player->last_name,
           player->overall);
}