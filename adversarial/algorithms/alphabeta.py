# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/18/2026
# project3
# alphabeta.py

from state import PLAYER
from rules import get_moves, make_move
from evaluation import evaluate
from algorithms.minimax import successors, cutoff_test

# Function Name: alphabeta
# Description:   carries out minimax search with alpha-beta pruning
# Parameters:    state - state tuple
#                depth_limit - maximum number of moves search can look
# Return Value:  dict with move, score, nodes_evaluated, and max_depth
def alphabeta(state, depth_limit):
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
        #updates metrics dict
        metrics["nodes_evaluated"] = metrics["nodes_evaluated"] + 1
        metrics["max_depth"] = max(metrics["max_depth"], depth)
        return evaluate(state, player, depth)

    # Function Name: max_value
    # Description:   finds the best score the root player can get, skips
    #                moves that dont change result
    # Parameters:    state - state tuple
    #                depth - how many moves deep the state is from current board
    #                alpha - best score found so far for the root player
    #                beta - lowest score found so far for the opponent
    # Return Value:  best score value
    def max_value(state, depth, alpha, beta):
        if cutoff_test(state, depth, depth_limit):
            return evaluate_state(state, depth)

        value = -float("inf")
        for child in successors(state):
            value = max(value, min_value(child, depth + 1, alpha, beta))
            #opponent has a better choice somewhere else, so stops early
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    # Function Name: min_value
    # Description:   finds the worst score the root player can get, skips
    #                moves that dont change result
    # Parameters:    state - state tuple
    #                depth - how many moves deep the state is from current board
    #                alpha - best score the root player is already sure of
    #                beta - lowest score found so far for the opponent
    # Return Value:  worst score value
    def min_value(state, depth, alpha, beta):
        if cutoff_test(state, depth, depth_limit):
            return evaluate_state(state, depth)

        value = float("inf")
        for child in successors(state):
            value = min(value, max_value(child, depth + 1, alpha, beta))
            #root player has a better choice somewhere else, so stops early
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    #tries every move and keeps the one with the best score after the opponent replies
    best_score = -float("inf")
    best_move = None
    alpha = -float("inf")
    beta = float("inf")
    for move in get_moves(state):
        score = min_value(make_move(state, move), 1, alpha, beta)
        #only replaces on a higher score, ties keep the lowest move
        if score > best_score:
            best_score = score
            best_move = move
        
        alpha = max(alpha, best_score)

    return {
        "move": best_move,
        "score": best_score,
        "nodes_evaluated": metrics["nodes_evaluated"],
        "max_depth": metrics["max_depth"],
    }