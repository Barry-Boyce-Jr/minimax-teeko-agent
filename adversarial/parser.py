# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/15/2026
# project3
# parser.py

from state import make_state

PIECES_PER_PLAYER = 5

# Function Name: parse
# Description:   Reads a game state line value by value, sorting each value
#                into the player, black's pieces, or red's pieces based on
#                where it falls in the line, and returns the parsed state
# Parameters:    line - game state line from stdin
# Return Value:  tuple:
#                player - "B" or "R",
#                black - black's  positions,
#                red - red's  positions

def parse(line):
    tuple_data = line.split()

    #first value is the player whose turn it is
    player = tuple_data.pop(0)

    #first 5 positions are Black's, the rest are Red's
    black = []
    red = []
    for position in tuple_data:
        if len(black) < PIECES_PER_PLAYER:
            black.append(int(position))
        else:
            red.append(int(position))

    #builds state, sorting each player's pieces
    return make_state(player, black, red)