#include "league.h"
#include "csv_parser.h"
#include "main_menu.h"
#include <stdio.h>

void league(){
    while(true){
        if(league_is_empty()){
            char choice;
            printf("Since the league is empty, would you like to generate a new league?\n");
            printf("1) Yes\n");
            printf("2) Go back to the main menu\n");
            printf("3) Refresh\n");
            scanf("%s", &choice);
            switch(choice){
                case '1':
                    generate_league();
                    return;
                case '2':
                    main_menu();
                    return;
                case '3':
                    break;
                default:
                    printf("Please type 1, 2, or 3");
            }
        }
    }
}

void generate_league(){
    printf("Generating league\n");

}