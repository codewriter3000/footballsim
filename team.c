#include "team.h"
#include "string.h"
#include <stdlib.h>
#include <stdio.h>

Team teams[TEAM_CAPACITY] = { 0 };
int num_of_teams = 0;

void generate_team(){
    Team tmp = { .city = fetch_city(),
                 .mascot = fetch_mascot() };
    print_team(&tmp);
    *(teams + num_of_teams++) = tmp;
}

char *fetch_city(){
    char *tmp = calloc(sizeof(char), 32);

    FILE *city_names = fopen("../data/city_names", "r");
    if(city_names == NULL)  printf("city_names not found\n");

    int r = rand() % (int)(990 * CITY_RARITY) + 1;
    char *line = calloc(32, sizeof(char));
    int l = 1, i = 0;
    char ch;
    do {
        ch = fgetc(city_names);
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
    fclose(city_names);
    return tmp;
}

char *fetch_mascot(){
    char *tmp = calloc(sizeof(char), 32);

    FILE *mascots = fopen("../data/mascots", "r");
    if(mascots == NULL)  printf("mascots not found\n");

    int r = rand() % 479 + 1;
    char *line = calloc(32, sizeof(char));
    int l = 1, i = 0;
    char ch;
    do {
        ch = fgetc(mascots);
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
    fclose(mascots);
    return tmp;
}

void print_team(Team *team){
    printf("%s, %s\n",
           team->city,
           team->mascot);
}