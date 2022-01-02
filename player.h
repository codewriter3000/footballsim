#include <bits/types/FILE.h>
#include <stdbool.h>

#ifndef _PLAYER__H
#define _PLAYER__H

#define PLAYER_CAPACITY 2000        // the maximum player capacity
#define FIRST_NAME_RARITY 0.3       // higher the percentage, more likely you'll get rare first names
#define LAST_NAME_RARITY 0.1        // higher the percentage, more likely you'll get rare last names

typedef struct {                    // what a player is composed of
    char *first_name, *last_name;
    int overall;
    bool is_offense;
} Player;

extern Player players[PLAYER_CAPACITY];             // an array of players
extern int num_of_players;
void clear_players();
void generate_player();             // randomly generates a player and returns that player

double bell_curve(int);
char *fetch_first_name();           // fetches first name from the source file of first names
char *fetch_last_name();            // see above
int fetch_overall();               // fetches overall from a bell curve function

char *get_position(Player*, bool);
void print_player(Player*);           // prints player and info about the player

#endif