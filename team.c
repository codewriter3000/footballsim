#include "team.h"
#include "string.h"
#include <stdlib.h>
#include <stdio.h>

Team teams[TEAM_CAPACITY] = { 0 };
int num_of_teams = 0;

void clear_teams(){
    memset(teams, 0, sizeof teams);
    num_of_teams= 0;
}

void generate_team(){
    Team tmp = { .city = fetch_city(),
                 .mascot = fetch_mascot()};
    tmp.coach = generate_coach()
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
    printf("%s %s\n",
           team->city,
           team->mascot);
}

void print_full_team(Team *team){
    printf("The %s %s, coached by %s %s\n",
           team->city,
           team->mascot,
           team->coach.first_name,
           team->coach.last_name);
}

void write_team(FILE *fp, Team *team){
    char buffer[68];
    snprintf(buffer, 68, "%s, %s, ",
             team->city,
             team->mascot);
    fputs(buffer, fp);
    write_coach(fp, &team->coach);
    for(int i = 0; i < ROSTER_CAPACITY - 1; i++){
        write_player(fp, &team->roster[i], false);
    }
    write_player(fp, &team->roster[ROSTER_CAPACITY-1], true);
}

void write_coach(FILE *fp, Coach *coach){
    char buffer[56];
    snprintf(buffer, 56, "%s, %s, %d, %f, ",
             coach->first_name,
             coach->last_name,
             coach->overall,
             coach->lean);
    fputs(buffer, fp);
}

void write_player(FILE *fp, Player *player, bool is_last){
    char buffer[102];
    if(!is_last){
        snprintf(buffer, 102, "%s, %s, %d, ",
                 player->first_name,
                 player->last_name,
                 player->overall);
    } else {
        snprintf(buffer, 101, "%s, %s, %d\n",
                 player->first_name,
                 player->last_name,
                 player->overall);
    }
    fputs(buffer, fp);
}

char *get_team_name(Team *team){
    char *tmp = calloc(49, sizeof(char));
    sprintf(tmp, "%s%s", team->city, team->mascot);
    return tmp;
}

double average_ovr(Team *team){
    int sum = 0;
    for(int i = 0; i < ROSTER_CAPACITY; i++){
        sum += team->roster[i].overall;
    }
    return sum * 1.0/ROSTER_CAPACITY;
}