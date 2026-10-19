# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/18/2026
# project3
# minimax.py


from state import PLAYER
from rules import get_moves, make_move, terminal_test
from evaluation import evaluate

# Function Name: successors
# Description:   builds every state reachable in one move
# Parameters:    state - state tuple
# Return Value:  list of child states
def successors(state):
    children = []
    for move in get_moves(state):
        children.append(make_move(state, move))
    return children

# Function Name: cutoff_test
# Description:   checks whether the search should stop at a state
# Parameters:    state - state tuple
#                depth - how many moves deep the state is from current board
#                depth_limit - maximum number of moves search can look
# Return Value:  true if the depth limit is reached or the game is over
def cutoff_test(state, depth, depth_limit):
    return depth >= depth_limit or terminal_test(state)

# Function Name: minimax
# Description:   carries out minimax search
# Parameters:    state - state tuple
#                depth_limit - maximum number of moves search can look
# Return Value:  dict with move, score, nodes_evaluated, and max_depth
def minimax(state, depth_limit):
    #root player saved
    player = state[PLAYER]
    #metrics reset every search
    metrics = {
        "nodes_evaluated": 0,
        "max_depth": 0
    }

    # Function Name: evaluate_state
    # Description:   scores a state with the evaluation function and updates
    #                the search metrics
    # Parameters:    state - state tuple
    #                depth - how many moves deep the state is from current board
    # Return Value:  score of the state
    def evaluate_state(state, depth):
        #updates the shared metrics dict
        metrics["nodes_evaluated"] = metrics["nodes_evaluated"] + 1
        metrics["max_depth"] = max(metrics["max_depth"], depth)
        return evaluate(state, player, depth)

    # Function Name: max_value
    # Description:   finds the best score the root player can get
    # Parameters:    state - state tuple
    #                depth - how many moves deep the state is from current board
    # Return Value:  best score
    def max_value(state, depth):
        if cutoff_test(state, depth, depth_limit):
            return evaluate_state(state, depth)

        value = -float("inf")
        for child in successors(state):
            value = max(value, min_value(child, depth + 1))
        return value

    # Function Name: min_value
    # Description:   finds the worst score for the root player
    # Parameters:    state - state tuple
    #                depth - how many moves deep the state is from current board
    # Return Value:  worst score
    def min_value(state, depth):
        if cutoff_test(state, depth, depth_limit):
            return evaluate_state(state, depth)

        value = float("inf")
        for child in successors(state):
            value = min(value, max_value(child, depth + 1))
        return value

    #tries every move and keeps the one with the best score after the opponent replies
    best_score = -float("inf")
    best_move = None
    for move in get_moves(state):
        score = min_value(make_move(state, move), 1)
         #only replaces on a higher score, ties keep the lowest move
        if score > best_score:
            best_score = score
            best_move = move

    return {
        "move": best_move,
        "score": best_score,
        "nodes_evaluated": metrics["nodes_evaluated"],
        "max_depth": metrics["max_depth"],
    }