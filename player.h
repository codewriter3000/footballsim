#include <bits/types/FILE.h>

#define PLAYER_CAPACITY 2000        // the maximum player capacity
#define FIRST_NAME_RARITY 0.5       // higher the percentage, more likely you'll get rare first names
#define LAST_NAME_RARITY 0.1        // higher the percentage, more likely you'll get rare last names

typedef struct {                    // what a player is composed of
    char *first_name, *last_name;
    int overall;
} Player;

extern Player players[PLAYER_CAPACITY];             // an array of players
extern int num_of_players;
void generate_player();             // randomly generates a player and returns that player

double bell_curve(int);
char *fetch_first_name();           // fetches first name from the source file of first names
char *fetch_last_name();            // see above
int fetch_overall();               // fetches overall from a bell curve function

void print_player(Player*);           // prints player and info about the player