# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/16/2026
# project3
# rules.py

from state import make_state, get_pieces, get_placed_pieces, convert_row_column, convert_square, on_board, NUM_SQUARES, PLAYER, BLACK_PIECES, RED_PIECES, BLACK, RED, UNPLACED, WIN_LENGTH, BOARD_SIZE


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

# Function Name: line_squares
# Description:   builds a line of 4 squares 
# Parameters:    row - starting row
#                column - starting column
#                row_step - row change for each step of the line
#                column_step - column change for each step of the line
# Return Value:  list of 4 squares or none if the line runs off the board
def line_squares(row, column, row_step, column_step):
    line = []
    for step in range(WIN_LENGTH):
        #stops if the line goes off the board
        if not on_board(row, column):
            return None
        line.append(convert_square(row, column))
        #moves one step in the line's direction
        row = row + row_step
        column = column + column_step
    return line

# Function Name: build_win_configurations
# Description:   lists every group of 4 squares that wins the game
# Parameters:    none
# Return Value:  list of lists of 4 squares
def build_win_configurations():
    configurations = []

    #horizontal lines
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            line = line_squares(row, column, 0, 1)
            if line is not None:
                configurations.append(line)

    #vertical lines
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            line = line_squares(row, column, 1, 0)
            if line is not None:
                configurations.append(line)

    #diagonal lines going down-right
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            line = line_squares(row, column, 1, 1)
            if line is not None:
                configurations.append(line)

    #diagonal lines going down-left
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            line = line_squares(row, column, 1, -1)
            if line is not None:
                configurations.append(line)

    #2x2 blocks
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            #skips blocks that run off board
            if not on_board(row + 1, column + 1):
                continue
            block = [convert_square(row, column), convert_square(row, column + 1),
                     convert_square(row + 1, column), convert_square(row + 1, column + 1)]
            configurations.append(block)

    #tilted squares
    for row in range(BOARD_SIZE):
        for column in range(BOARD_SIZE):
            #skips tilted squares whose center is on an edge
            if not on_board(row - 1, column - 1) or not on_board(row + 1, column + 1):
                continue
            tilted = [convert_square(row - 1, column), convert_square(row, column - 1),
                      convert_square(row, column + 1), convert_square(row + 1, column)]
            configurations.append(tilted)

    return configurations

WIN_CONFIGURATIONS = build_win_configurations()

# Function Name: is_win
# Description:   checks whether a player has 4 pieces in any winning shape
# Parameters:    state - state tuple
#                player - BLACK or RED
# Return Value:  true if the player has won, else false
def is_win(state, player):
    pieces = get_placed_pieces(state, player)
    for configuration in WIN_CONFIGURATIONS:
        #counts how many of the configuration's squares the player has
        count = 0
        for square in configuration:
            if square in pieces:
                count += 1
        if count == WIN_LENGTH:
            return True
    return False

# Function Name: terminal_test
# Description:   checks whether the game is over, either player has won or
#                the player to move has no legal moves
# Parameters:    state - state tuple
# Return Value:  true if the game is over, otherwise false
def terminal_test(state):
    if is_win(state, BLACK) or is_win(state, RED):
        return True
    return len(get_moves(state)) == 0