# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/17/2026
# project3
# evaluation.py


from state import NUM_SQUARES, WIN_LENGTH, player_switch, get_placed_pieces
from rules import WIN_CONFIGURATIONS, is_win

#score of a won game
WIN_SCORE = 1000000

#weights for each feature towards score
CENTER_WEIGHT = 1
SHAPE_WEIGHT = 1
FORK_WEIGHT = 500

#points for pieces in close to winning shape
ONE_PIECE_POINTS = 1
TWO_PIECE_POINTS = 10
THREE_PIECE_POINTS = 100

#different winning squares needed for a fork
FORK_SQUARES = 2

# Function Name: square_values
# Description:   counts how many win configurations each square is part of
# Parameters:    none
# Return Value:  dict of square to number of configurations
def square_values():
    values = {}
    for square in range(1, NUM_SQUARES + 1):
        values[square] = 0
    for configuration in WIN_CONFIGURATIONS:
        for square in configuration:
            values[square] = values[square] + 1
    return values

VALUES = square_values()

# Function Name: count_pieces
# Description:   counts a players pieces in one shape
# Parameters:    shape - list of 4 squares
#                player_pieces - list of the players placed pieces
#                opponent_pieces - list of the opponents placed pieces
# Return Value:  number of the player's pieces, none if the opponent
#                has a piece in it
def count_pieces(shape, player_pieces, opponent_pieces):
    count = 0
    for square in shape:
        if square in opponent_pieces:
            return None
        if square in player_pieces:
            count = count + 1
    return count

# Function Name: center_score
# Description:   adds up the value of every square the player has a piece on
# Parameters:    state - state tuple
#                player - BLACK or RED
# Return Value:  center control score
def center_score(state, player):
    total = 0
    for square in get_placed_pieces(state, player):
        total = total + VALUES[square]
    return total

# Function Name: shape_score
# Description:   scores how close the player is to finishing each
#                configuration the opponent has not blocked
# Parameters:    state - state tuple
#                player - BLACK or RED
# Return Value:  shape potential score
def shape_score(state, player):
    player_pieces = get_placed_pieces(state, player)
    opponent_pieces = get_placed_pieces(state, player_switch(player))
    total = 0
    for configuration in WIN_CONFIGURATIONS:
        count = count_pieces(configuration, player_pieces, opponent_pieces)
        #skips shapes the opponent has blocked
        if count is None:
            continue
        if count == 1:
            total = total + ONE_PIECE_POINTS
        elif count == 2:
            total = total + TWO_PIECE_POINTS
        elif count == 3:
            total = total + THREE_PIECE_POINTS
    return total

# Function Name: fork_score
# Description:   checks whether the player has two or more different squares
#                that would each win
# Parameters:    state - state tuple
#                player - BLACK or RED
# Return Value:  1 if the player has a fork,  0 if not
def fork_score(state, player):
    player_pieces = get_placed_pieces(state, player)
    opponent_pieces = get_placed_pieces(state, player_switch(player))
    winning_squares = []
    for configuration in WIN_CONFIGURATIONS:
        if count_pieces(configuration, player_pieces, opponent_pieces) == WIN_LENGTH - 1:
            #finds the one empty square that would finish it
            for square in configuration:
                if square not in player_pieces and square not in winning_squares:
                    winning_squares.append(square)
    if len(winning_squares) >= FORK_SQUARES:
        return 1
    return 0

# Function Name: evaluate
# Description:   scores a state from the players point of view
# Parameters:    state - state tuple
#                player - BLACK or RED
#                depth - how many moves deep the state is
# Return Value:  score for a won or lost game, or the weighted sum of center control
#                shape potential, and forks
def evaluate(state, player, depth):
    opponent = player_switch(player)
    #wins found sooner score higher, losses found later score higher
    if is_win(state, player):
        return WIN_SCORE - depth
    if is_win(state, opponent):
        return -WIN_SCORE + depth

    #each component is the players score minus the opponents score
    center_control = center_score(state, player) - center_score(state, opponent)
    shape_potential = shape_score(state, player) - shape_score(state, opponent)
    fork_detection = fork_score(state, player) - fork_score(state, opponent)
    return (CENTER_WEIGHT * center_control + SHAPE_WEIGHT * shape_potential + FORK_WEIGHT * fork_detection)