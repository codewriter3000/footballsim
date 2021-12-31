#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "team.h"
#include "csv_parser.h"

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
        default:
            switch(column % 3){
                case 0:
                    team->roster[(int)(column/3)-1].first_name = calloc(16, sizeof(char));
                    strcpy(team->roster[(int)(column/3)-1].first_name, field);
                    break;
                case 1:
                    team->roster[(int)(column/3)-1].last_name = calloc(32, sizeof(char));
                    strcpy(team->roster[(int)(column/3)-1].last_name, field);
                    break;
                case 2:
                    team->roster[(int)(column/3)-1].overall = atoi(field);
                    //printf("ovr: %d\n", team->roster[(int)(column/3)+1].overall);
                    break;
            }
    }
}