# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/15/2026
# project3
# main.py

import sys
from parser import parse
from algorithms.minimax import minimax
from algorithms.alphabeta import alphabeta

#move sent when no legal move exists (like the reference file given for project 3 does)
NO_MOVE = (0, 1)

#error if usage incorrect
if len(sys.argv) < 3:
    print("Usage: python3 main.py <minimax|alphabeta> <depth>", file=sys.stderr)
    sys.exit(1)

#saves cla 
algorithm = sys.argv[1]
depth = int(sys.argv[2])

#error for algorithm cla
if algorithm != "minimax" and algorithm != "alphabeta":
    print("algorithm must be 'minimax' or 'alphabeta'", file=sys.stderr)
    sys.exit(1)

#reads one state per line until the file ends
for line in sys.stdin:
    #skips blank lines
    if not line.strip():
        continue
    state = parse(line)

    #all searches
    if algorithm == "minimax":
        result = minimax(state, depth)
    elif algorithm == "alphabeta":
        result = alphabeta(state, depth)

    #if no legal move found
    if result["move"] is not None:
        move = result["move"]
    else:
        move = NO_MOVE

    #writes move to stdout and metrics to stderr. flushes buffer 
    print(f"{move[0]} {move[1]}", flush=True)
    print(f"{algorithm},{result['nodes_evaluated']},{result['max_depth']},{result['score']}",
          file=sys.stderr, flush=True)