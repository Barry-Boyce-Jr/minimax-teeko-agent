# Barry Boyce Jr
# CPSC 447
# Fall 2026
# 10/19/2026
# project3
# benchmark.py


import csv
import subprocess
import time

#the max seconds one run can take, can be changed, higher time limit increases time for benchmark.py to finish running
TIME_LIMIT = 300

# Function Name: run_test
# Description:   Runs one search algorithm on a state, stopping it once it
#                runs longer than TIME_LIMIT seconds
# Parameters:    algorithm - "minimax" or "alphabeta"
#                depth - search depth limit
#                line - game state line
# Return Value:  algorithm, nodes evaluated, max depth, chosen move score, seconds,
#                or "limit" for each if the search was stopped
def run_test(algorithm, depth, line):
    start = time.perf_counter()

    #if stopped early from time then return limit
    try:
        run = subprocess.run(["python3", "main.py", algorithm, str(depth)],
                             input=line, capture_output=True, text=True, timeout=TIME_LIMIT)
    except subprocess.TimeoutExpired:
        return algorithm, "limit", "limit", "limit", "limit"

    seconds = round(time.perf_counter() - start, 4)

    #if the agent crashed there is no metrics row
    if run.returncode != 0:
        return algorithm, "failed", "failed", "failed", seconds

    metrics = run.stderr.strip().split(",")
    return metrics[0], metrics[1], metrics[2], metrics[3], seconds

# all combinations of test files
# (phase, state count)
conditions = [("drop", 14), ("slide", 14)]
depths = [1, 2, 3]
algorithms = ["minimax", "alphabeta"]

# loops through all test files & outputs results
with open("benchmark_results.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["algorithm", "nodes_evaluated", "max_depth", "chosen_move_score",
                     "test_file", "phase", "depth_limit", "time_seconds"])
    for phase, count in conditions:
        for test_number in range(1, count + 1):
            test_file = f"{phase}_{test_number}.txt"
            with open(f"testing/{test_file}", "r") as file:
                line = file.read()
            for depth in depths:
                for algorithm in algorithms:
                    agent, nodes_evaluated, max_depth, score, seconds = run_test(algorithm, depth, line)
                    writer.writerow([agent, nodes_evaluated, max_depth, score,
                                     test_file, phase, depth, seconds])
                    print(f"{algorithm} depth {depth} search for {test_file} complete")     # progress