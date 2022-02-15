#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "team.h"
#include "csv_parser.h"

bool league_is_empty(){
    FILE *fp = fopen("../data/output/leaguedata", "r");
    return ftell(fp) == 0;
}

void parse_league(){
    FILE *fp = fopen("../data/output/leaguedata", "r");
    char *tmp = calloc(64, sizeof(char));
    char ch;
    int record = 1;
    int column = 1;
    int i = 0;
    do {
        ch = fgetc(fp);
        switch(ch){
            case '\n':
                tmp[i] = '\0';
                process_field(record, column, tmp);
                record++;
                column = 1;
                i = 0;
                break;
            case ',':
                tmp[i] = '\0';
                process_field(record, column, tmp);
                column++;
                i = 0;
                break;
            default:
                tmp[i++] = ch;
        }
    } while((int)ch != -1);
    free(tmp);
}

void parse_teams(){
    FILE *fp = fopen("../data/output/teamdata", "r");
    char *tmp = calloc(64, sizeof(char));
    char ch;
    int record = 1;
    int column = 1;
    int i = 0;
    do {
        ch = fgetc(fp);
        switch(ch){
            case '\n':
                tmp[i] = '\0';
                process_field(record, column, tmp);
                record++;
                column = 1;
                i = 0;
                break;
            case ',':
                tmp[i] = '\0';
                process_field(record, column, tmp);
                column++;
                i = 0;
                break;
            default:
                tmp[i++] = ch;
        }
    } while((int)ch != -1);
    free(tmp);
}

void process_field(int record, int column, char *field){
    Team *team = &teams[record-1];
    switch(column){
        case 1:
            team->city = calloc(32, sizeof(char));
            strcpy(team->city, field);
            break;
        case 2:
            team->mascot = calloc(32, sizeof(char));
            strcpy(team->mascot, field);
            break;
        case 3:
            team->coach.first_name = calloc(16, sizeof(char));
            strcpy(team->coach.first_name, field);
            break;
        case 4:
            team->coach.last_name = calloc(16, sizeof(char));
            strcpy(team->coach.last_name, field);
            break;
        case 5:
            team->coach.overall = atoi(field);
            break;
        case 6:
            team->coach.lean = atof(field);
            break;
        default:
            switch((column-3) % 4){
                case 0:
                    team->roster[(int)((column-3)/4-1)].first_name = calloc(16, sizeof(char));
                    strcpy(team->roster[(int)((column-3)/4-1)].first_name, field);
                    break;
                case 1:
                    // bug starts here
                    team->roster[(int)((column-3)/4-1)].last_name = calloc(32, sizeof(char));
                    strcpy(team->roster[(int)((column-3)/4-1)].last_name, field);
                    break;
                case 2:
                    team->roster[(int)((column-3)/4-1)].overall = atoi(field);
                    break;
                case 3:
                    //printf("field: %s\n", field);
                    //printf("position: %d\n", field[1] == 'O');
                    team->roster[(int)((column-3)/4-1)].is_offense = field[1] == 'O';
                    break;
            }
    }
}