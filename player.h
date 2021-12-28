#include <bits/types/FILE.h>

#define PLAYER_CAPACITY 1024        // the maximum player capacity

typedef struct {                    // what a player is composed of
    char *first_name, *last_name;
    int overall;
} Player;

FILE *first_names;
FILE *last_names;

static Player *players;             // an array of players
void generate_player();             // randomly generates a player and returns that player

double bell_curve(int);
char *fetch_first_name();           // fetches first name from the source file of first names
char *fetch_last_name();            // see above
int fetch_overall();               // fetches overall from a bell curve function