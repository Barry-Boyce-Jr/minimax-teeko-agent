# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/15/2026
# project3
# state.py

BOARD_SIZE = 6
PLAYER = 0
BLACK_PIECES = 1
RED_PIECES = 2
BLACK = "B"
RED = "R"
UNPLACED = 0

# Function Name: make_state
# Description:   builds a state, sorting each player's pieces in ascending order
# Parameters:    player -  either black or red depending on which player's turn it is
#                black - list of the positions for black
#                red - list of hte positions for red
# Return Value:  state tuple (player, black, red)
def make_state(player, black, red):
    return (player, tuple(sorted(black)), tuple(sorted(red)))


# Function Name: get_pieces
# Description:   gets one player's pieces from a state
# Parameters:    state - state tuple
#                player - BLACK or RED
# Return Value:  sorted tuple of that player's positions
def get_pieces(state, player):
    if player == BLACK:
        return state[BLACK_PIECES]
    return state[RED_PIECES]

# Function Name: get_placed_pieces
# Description:   gets the pieces a player has already put on the board
# Parameters:    state - state tuple
#                player - BLACK or RED
# Return Value:  list of positions of pieces, skips the unplaced pieces
def get_placed_pieces(state, player):
    placed = []
    for square in get_pieces(state, player):
        if square != UNPLACED:
            placed.append(square)
    return placed

# Function Name: convert_row_column
# Description:   converts a board position to a row and column
# Parameters:    square - position on board
# Return Value:  (row, column), both starting at 0
def convert_row_column(square):
    #starts index for squares at 0 instead of 1
    index = square - 1
    return (index // BOARD_SIZE, index % BOARD_SIZE)

# Function Name: convert_square
# Description:   converts a row and column to a board position
# Parameters:    row - row starting at 0
#                column - column starting at 0
# Return Value:  position from 1 to 36
def convert_square(row, column):
    return row * BOARD_SIZE + column + 1

# Function Name: on_board
# Description:   checks whether a row and column are inside the board
# Parameters:    row - row starting at 0
#                column - column starting at 0
# Return Value:  true if on the board, otherwise false
def on_board(row, column):
    return 0 <= row < BOARD_SIZE and 0 <= column < BOARD_SIZE