# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/16/2026
# project3
# rules.py

from state import make_state, get_pieces, get_placed_pieces, convert_row_column, convert_square, on_board, NUM_SQUARES, PLAYER, BLACK_PIECES, RED_PIECES, BLACK, RED, UNPLACED


DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

# Function Name: touching_squares
# Description:   finds the touching squares of every square once
# Parameters:    none
# Return Value:  dict of list of touching squares
def touching_squares():
    adjacent = {}
    for square in range(1, NUM_SQUARES + 1):
        row, column = convert_row_column(square)

        touching = []
        for row_step, column_step in DIRECTIONS:
            new_row = row + row_step
            new_column = column + column_step

            #skips steps that go off the board
            if not on_board(new_row, new_column):
                continue

            touching.append(convert_square(new_row, new_column))

        touching.sort()
        adjacent[square] = touching

    return adjacent

ADJACENT = touching_squares()

# Function Name: can_move
# Description:   checks whether the player can move drop or slide
#                a piece 
# Parameters:    state - state tuple
#                occupied - list of squares that have a piece on them
#                current - square to move from
#                target - square to move to
# Return Value:  true if the move is possible, false if not
def can_move(state, occupied, current, target):
    pieces = get_pieces(state, state[PLAYER])

    if target in occupied:
        return False
    #drop phase
    elif UNPLACED in pieces and current != UNPLACED:
        return False
    #slide phase
    elif UNPLACED not in pieces and current not in pieces:
        return False
    #slides can only go to a touching square
    elif current != UNPLACED and target not in ADJACENT[current]:
        return False
    return True

# Function Name: get_moves
# Description:   Lists every legal move for the player to move
# Parameters:    state - state tuple
# Return Value:  sorted list of (current, target) tuples

def get_moves(state):
    pieces = get_pieces(state, state[PLAYER])
    occupied = get_placed_pieces(state, BLACK) + get_placed_pieces(state, RED)

    #drops all come from 0, slides come from each placed piece
    if UNPLACED in pieces:
        current_squares = [UNPLACED]
    else:
        current_squares = pieces

    #finds all moves
    moves = []
    for current in current_squares:
        #drops can go anywhere, slides only to touching squares
        if current == UNPLACED:
            targets = range(1, NUM_SQUARES + 1)
        else:
            targets = ADJACENT[current]

        for target in targets:
            #skips invalid moves
            if not can_move(state, occupied, current, target):
                continue
            moves.append((current, target))

    #sorts moves by current, then target
    moves.sort()

    #returns moves
    return moves

# Function Name: make_move
# Description:   Builds the new state after the player to move drops or
#                slides a piece, then passes the turn
# Parameters:    state - state tuple
#                next_move - (current, target) tuple, current is 0 for dropping a piece
# Return Value:  new state tuple
def make_move(state, next_move):
    player = state[PLAYER]
    current = next_move[0]
    target = next_move[1]

    pieces = []
    for piece in get_pieces(state, player):
        pieces.append(piece)

    pieces.remove(current)
    pieces.append(target)

# makes state when turn is passed to the next player
    if player == BLACK:
        new_state = make_state(RED, pieces, state[RED_PIECES])
    else:
        new_state = make_state(BLACK, state[BLACK_PIECES], pieces)
    return new_state