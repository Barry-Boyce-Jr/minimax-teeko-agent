Barry Boyce Jr
CPSC 447
Fall 2026
Project 3
10/19/2026
purpose: gives instructions how to run code, gives credit, and explains designs choices and results

REQUIREMENTS
    Python 3

HOW TO RUN
    1. navigate to adversarial directory `project3\adversarial`
    2. enter CLA `python main.py <minimax|alphabeta> <depth> < testing/drop_1.txt`
        (this can be recreated with any file from testing dir)
        (the chosen move is printed to stdout as `0 TARGET` for a drop or `FROM TO` for a slide)
        (the metrics row algorithm,nodes_evaluated,max_depth,chosen_move_score is printed to stderr)
        (main.py keeps reading one state per line until the input ends, so it can stay open for a whole game)
        (on Linux/Mac use `python3`, in PowerShell `<` doesn't work so use
        `Get-Content testing/drop_1.txt | python main.py <minimax|alphabeta> <depth>`)
    3. enter CLA `python benchmark.py`
        (benchmark_results.csv will be recreated each run, located in adversarial dir)
        (this runs minimax and alphabeta at depths 1, 2, and 3 against all 28 test states in testing)
        (main.py is run as a subprocess and the metrics row it writes to stderr is captured and written to the csv
        along with the test file, phase, depth limit, and time in seconds)
        (any run that takes longer than TIME_LIMIT = 300 seconds is stopped and recorded as limit, this can be
        changed by changing the value of TIME_LIMIT in benchmark.py. This will result in longer times)

CREDIT
    Chapter 6 Lecture notes used as guide for minimax, alpha-beta pruning, cutoff test, and evaluation functions
    AIMA algorithms textbook (shown in class) used to check minimax and alpha-beta
    Dr. Schwesinger's ttt.py used as the starting structure for minimax (max_value and min_value inside the search)
    project 2 used as the starting structure for main.py, parser.py, benchmark.py, and the
    algorithms folder
    Dr. Schwesinger's runner, random_player.cpp, and cli_player.cpp used to check input, output, and game rules
    Claude AI assisted with reviewing code against the reference and rubric, the evaluation function,
    the benchmark time limit, ideas for functions that would be useful in state.py and README table layouts/ theoretical concepts
    as well as assistance with wording of readme file.
    Claude AI assisted in drafting rules.py design 
    Claude AI fully wrote test files found in `project3\adversarial\testing`

NOTE
    I was instructed to begin this project earlier than I did (October 15) and did not submit a check-in (October 12) for my project against
    instruction from Dr. Schwesinger. I apologize for the inconvenience 

STATE-SPACE DESIGN
   The file structure was built off of Project 2, so state.py, parser.py, main.py, benchmark.py, and the
   algorithms folder all do the same jobs they did before. The state itself is different, since a game state
   doesn't need a path back to the start like the blocks world did, so there is no Node class or closed set.
   The search only needs the current board and whose turn it is.

   the state is a tuple (player, black, red), where player is "B" or "R" for whose turn it is, and black and red
   are tuples of each player's 5 squares. The board squares are numbered 1 to 36 from the top left to the bottom
   right, so row 1 is 1-6, row 2 is 7-12, and so on, and a piece that hasn't been dropped yet is 0. For example,
   the starting state B 0 0 0 0 0 0 0 0 0 0 is ("B", (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)). parse splits the input
   line, takes the first value as the player, the next 5 numbers as black, and the last 5 as red, and make_state
   sorts each player's pieces so the 0s always stay first, so R 5 0 12 0 0 0 20 0 0 0 becomes
   ("R", (0, 0, 0, 5, 12), (0, 0, 0, 0, 20)). The same board always makes the same tuple no matter what order the
   pieces come in convert_row_column turns a square into a row and column and convert_square goes back the other way,
   but these are only used to build the touching squares and win configurations once.

   The phase is decided by the player whose turn it is. If they still have a 0, every move is a drop (0, target)
   onto an empty square, and if they don't, every move is a slide (current, target) onto an empty square touching
   current horizontally, vertically, or diagonally. This means Red can still be dropping its last piece while
   Black has all 5 on the board, the same as the reference random_player.cpp. Moves are always in the same order,
   drops sorted by target and slides sorted by current then by target, so that results match the order the
   assignment requires. A player wins with 4 pieces in any of the 95 win configurations, which are 18 horizontal
   lines, 18 vertical lines, 18 diagonal lines (9 each way), 25 2x2 blocks, and 16 tilted squares (the 4 squares
   above, left, right, and below a center square). The game is over when either player has won or the player to
   move has no legal moves, and if there are no legal moves main.py sends 0 1 like the reference players.

   Both searches follow the Chapter 6 Minimax-Decision. The root tries every move and keeps the one whose
   min_value is highest, and max_value and min_value call each other going down the tree. Like ttt.py 
   (which is provided by Dr. Schwesinger) they're inside the search function so they can see the root player,
   so every score is from the point of view of the player to move. The search can't go to the end of the game, so like
   the Resource limits slide cutoff_test is used instead of the terminal test (it stops at the depth limit or when the game is over),
   and the evaluation function is used instead of the utility. alphabeta.py is the same as minimax.py except for alpha (the best
   score the root player can already get) and beta (the lowest score the opponent can already hold it to).
   max_value stops as soon as its value is at least beta and min_value stops as soon as its value is at most
   alpha, since the other player would never let the game get there. The best move is only replaced when a score
   is strictly higher, so when moves tie the first one in the sorted order (the lowest numbered one) is kept.

   nodes_evaluated counts every state the evaluation function scores, which only happens at a cutoff,
   max_depth is the deepest turn where a state was scored, and chosen_move_score is the score of the move that
   was picked. These are kept in a dict that is reset every search, since the runner keeps the same process
   open for the whole game. These were checked against the reference runner, where alphabeta at depth 3 beat
   random_player as both Black and Red with every move accepted, and the stderr row showing up next to each
   move (for example Turn 007 [B]: Move (0 8) | Stderr: alphabeta,1515,3,999999).

EVALUATION FUNCTION DESIGN
   Both minimax and alphabeta use the same evaluate(state, player, depth) function, only the search changes. A
   won game scores WIN_SCORE - depth and a lost game scores -WIN_SCORE + depth, where WIN_SCORE = 1,000,000.
   Taking off the depth makes a win found sooner score higher than one found later, and a loss found later
   score higher than one found sooner, so 999,999 means a win on the next move and 999,997 means a win that can
   be forced in 3 moves.

   Every other state is scored with the weighted linear sum from the Chapter 6 slideshow.
   Eval(s) = w1 * f1(s) + w2 * f2(s) + w3 * f3(s)
        = CENTER_WEIGHT * center control + SHAPE_WEIGHT * shape potential + FORK_WEIGHT * fork detection
   Like the slide's (number of white queens) - (number of black queens), each feature is the player's score
   minus the opponent's score, so the same function works for both players.

   Center control (CENTER_WEIGHT = 1) gives each square a value equal to the number of win configurations it's
   part of, and adds up the values of the squares a player's pieces are on. Corners are only part of 4
   configurations while the 4 middle squares are part of 19, since the middle squares are in more rows,
   diagonals, blocks, and tilted squares. The values are counted from the win configurations instead of being
   typed in, so they always match the win rules.
        | 4 | 7  | 8  | 8  | 7  | 4 |
        | 7 | 12 | 15 | 15 | 12 | 7 |
        | 8 | 15 | 19 | 19 | 15 | 8 |
        | 8 | 15 | 19 | 19 | 15 | 8 |
        | 7 | 12 | 15 | 15 | 12 | 7 |
        | 4 | 7  | 8  | 8  | 7  | 4 |

   Shape potential (SHAPE_WEIGHT = 1) goes through all 95 win configurations, the rows, columns, diagonals, 2x2
   blocks, and tilted squares, and skips any the opponent has a piece in, since those can never be won. An open
   configuration with 1, 2, or 3 of the player's pieces is worth 1, 10, or 100 points. Each extra piece is worth
   10 times more since it's that much closer to a win, so one open 3 (100) is worth more than a few open 2s.

   Fork detection (FORK_WEIGHT = 500) checks whether a player has 2 or more different empty squares that would
   each finish a win (open configurations with 3 pieces). The opponent can only block one square per move, so a
   fork is usually a win. It counts different squares and not configurations, since two configurations finished
   by the same square can be blocked with one move. FORK_WEIGHT is 500 so a fork counts for more than any normal
   difference in shape potential, so making a fork or stopping one comes before everything except a win or loss.
   For example, Black alone on square 15 scores 38, which is 19 for center control plus 19 for shape potential
   (square 15 is in 19 open configurations with 1 piece each).

SEARCH ANALYSIS
    Test states
    | Series        | Tests                      | What changes                                        | Phase |
    |---------------|----------------------------|-----------------------------------------------------|-------|
    | general       | drop_1-3, slide_1, slide_4 | empty board, first moves, scattered, crowded center | both  |
    | wins          | drop_4, drop_7-11          | diagonal, horizontal, vertical, 2x2, tilted square  | drop  |
    | wins          | slide_2, slide_5-8         | horizontal, vertical (Black and Red), diagonal,     | slide |
    |               |                            | tilted square                                       |       |
    | blocks        | drop_5, drop_12            | Black must block, Red must block a 2x2 block        | drop  |
    | blocks        | slide_3, slide_9           | Red must block, Red must block a tilted square      | slide |
    | forks         | drop_13, slide_12          | three in a row with both ends open                  | both  |
    | input/phase   | drop_6, drop_14, slide_14  | unsorted input, Red drops while Black is done,      | both  |
    |               |                            | first slide after the drop phase                    |       |
    | mobility      | slide_10, slide_11,        | boxed in piece, pieces sliding back and forth,      | slide |
    |               | slide_13                   | pieces on corners and edges                         |       |

    Table 1. Drop Phase — Nodes Evaluated vs. Search Depth
    | Test    | Moves | Minimax d2 | Alpha-Beta d2 | Minimax d3 | Alpha-Beta d3 |
    |---------|-------|------------|---------------|------------|---------------|
    | drop_1  | 36    | 1,260      | 449           | 42,840     | 8,157         |
    | drop_2  | 35    | 1,190      | 537           | 39,270     | 7,582         |
    | drop_3  | 32    | 992        | 248           | 29,760     | 2,216         |
    | drop_4  | 30    | 814        | 30            | 22,738     | 786           |
    | drop_5  | 30    | 870        | 530           | 23,577     | 5,591         |
    | drop_6  | 33    | 1,056      | 371           | 32,736     | 4,249         |
    | drop_7  | 30    | 842        | 266           | 23,549     | 2,110         |
    | drop_8  | 30    | 842        | 160           | 23,549     | 1,492         |
    | drop_9  | 30    | 842        | 270           | 23,549     | 1,512         |
    | drop_10 | 30    | 842        | 156           | 23,549     | 1,048         |
    | drop_11 | 30    | 842        | 134           | 23,549     | 933           |
    | drop_12 | 31    | 930        | 228           | 26,130     | 3,521         |
    | drop_13 | 32    | 992        | 278           | 29,760     | 2,817         |
    | drop_14 | 27    | 598        | 151           | 11,642     | 1,240         |

    Table 2. Slide Phase — Nodes Evaluated vs. Search Depth
    | Test     | Moves | Minimax d2 | Alpha-Beta d2 | Minimax d3 | Alpha-Beta d3 |
    |----------|-------|------------|---------------|------------|---------------|
    | slide_1  | 17    | 351        | 88            | 6,496      | 1,003         |
    | slide_2  | 22    | 508        | 184           | 11,446     | 1,845         |
    | slide_3  | 23    | 527        | 362           | 11,880     | 4,360         |
    | slide_4  | 14    | 286        | 120           | 5,319      | 1,630         |
    | slide_5  | 20    | 401        | 113           | 8,191      | 1,036         |
    | slide_6  | 28    | 612        | 176           | 16,377     | 2,433         |
    | slide_7  | 19    | 366        | 133           | 7,493      | 1,490         |
    | slide_8  | 27    | 358        | 74            | 9,616      | 1,050         |
    | slide_9  | 16    | 409        | 231           | 6,709      | 1,442         |
    | slide_10 | 15    | 223        | 56            | 3,762      | 641           |
    | slide_11 | 15    | 203        | 88            | 3,559      | 792           |
    | slide_12 | 29    | 486        | 85            | 13,587     | 1,149         |
    | slide_13 | 13    | 267        | 187           | 3,994      | 1,252         |
    | slide_14 | 23    | 485        | 112           | 11,442     | 1,726         |
    (Moves is the number of legal moves, which is also the nodes evaluated at depth 1 for both searches)

    Table 3. Totals — Nodes Evaluated & Time vs. Search Depth (all 14 states in each phase)
    | Phase | Depth | Minimax Nodes | Alpha-Beta Nodes | Fewer  | Minimax Time | Alpha-Beta Time |
    |-------|-------|---------------|------------------|--------|--------------|-----------------|
    | drop  | 1     | 436           | 436              | 0.0%   | 0.6 s        | 0.7 s           |
    | drop  | 2     | 12,912        | 3,808            | 70.5%  | 2.3 s        | 1.1 s           |
    | drop  | 3     | 376,198       | 43,254           | 88.5%  | 52.3 s       | 6.6 s           |
    | slide | 1     | 281           | 281              | 0.0%   | 0.6 s        | 0.6 s           |
    | slide | 2     | 5,482         | 2,009            | 63.4%  | 1.5 s        | 0.9 s           |
    | slide | 3     | 119,871       | 21,849           | 81.8%  | 19.9 s       | 4.2 s           |

    From Tables 1 and 2 we can see how much alpha-beta cuts down the search. At depth 1 both evaluate the same
    number of states, since there is only one level and nothing to prune. From depth 2 on, alpha-beta evaluated
    fewer states than minimax on every test, between 1.4x (slide_13) and 27x (drop_4) fewer at depth 2 and
    between 2.7x (slide_3) and 29x (drop_4) fewer at depth 3. Table 3 shows the gap getting bigger with depth,
    alpha-beta evaluated 70.5% fewer drop states at depth 2 and 88.5% fewer at depth 3, and 63.4% and 81.8% fewer
    slide states. Across all 28 states at depth 3, minimax evaluated 496,069 states and alpha-beta only 65,103
    (about 87% fewer), and on the empty board (drop_1) the time went from 5.1 seconds to 1.0 second.

    Tables 1 and 2 also show that pruning works best when the best move comes first. drop_4 is the biggest
    difference, where Black's winning move 0 1 is the very first move in the sorted order, so once it scores
    999,999 every other root move gets cut off after one reply and alpha-beta only evaluates 786 states instead
    of 22,738 (about 29x fewer). The other win tests (drop_7 to drop_11) are all between 11x and 25x fewer for
    the same reason. slide_3 is the smallest difference at depth 3 (about 2.7x fewer), where Red's only good move
    is a block from square 16, which comes after every move from squares 14 and 15 in the sorted order. The
    assignment requires moves to be sorted by square number and not by how good they are, so alpha-beta can't
    always try the best move first.

    Table 1 doesn't go down evenly with the number of moves, drop_7 to drop_11 all have 30 legal moves but minimax
    only evaluates 23,549 states at depth 3 instead of 30 x 29 x 28 = 24,360. This is because any branch where a
    player completes a win is scored right away by cutoff_test instead of being searched deeper, so tests with a
    win available have smaller trees than their number of moves would suggest.

    Depth 4 isn't in the benchmark since unpruned minimax takes about 1-2 minutes per drop state there. On the
    empty board minimax evaluates 1,413,720 states at depth 4 while alpha-beta evaluates 87,012 (about 94% fewer),
    which is another case of the gap growing with depth. (This can be replicated by changing depths to
    [1, 2, 3, 4] in benchmark.py, which takes about 30 minutes)

THEORETICAL VS. EMPIRICAL COMPLEXITY
    The Chapter 6 lecture notes say minimax's time is O(b^m), where b is the branching factor and m is the depth,
    and that with perfect move ordering alpha-beta's time is O(b^(m/2)), which doubles how deep it can search in
    the same time. The AIMA textbook also says that with random move ordering alpha-beta is about O(b^(3m/4)).

    The branching factor (the number of legal moves) is the Moves column in Tables 1 and 2. In the drop phase it
    starts at 36 and goes down by 1 with every piece dropped, and it averages 31.1 across the drop tests. In the
    slide phase each piece can move to at most 8 touching squares, but most of those are taken or off the board,
    so it's between 13 and 29 and averages 20.1. The number of states in a full tree grows very fast with depth,
    as shown in Table 4.

        Table 4. Full Tree Size vs. Depth (empty board, b = 36, 35, 34, ...)
        | Depth | States in Full Tree | Minimax Evaluated | Alpha-Beta Evaluated |
        |-------|---------------------|-------------------|----------------------|
        | 1     | 36                  | 36                | 36                   |
        | 2     | 1,260               | 1,260             | 449                  |
        | 3     | 42,840              | 42,840            | 8,157                |
        | 4     | 1,413,720           | 1,413,720         | 87,012               |

    Minimax matches O(b^m) exactly, it evaluates every state in the full tree, so each extra depth multiplies the
    work by about b (35x from depth 1 to 2 and 34x from depth 2 to 3 on the empty board). Alpha-beta grows a lot
    slower, about 12x from depth 1 to 2 and 18x from depth 2 to 3. Taking the cube root of the average nodes
    evaluated at depth 3 gives an effective branching factor of 14.6 for alpha-beta in the drop phase (30.0 for
    minimax) and 11.6 in the slide phase (20.5 for minimax), which is about b^0.79 per level. That's between the
    perfect ordering O(b^(m/2)) and minimax's O(b^m), and close to the random ordering O(b^(3m/4)), which makes
    sense since sorting moves by square number has nothing to do with how good a move is. With perfect ordering
    a depth 3 drop search would only need about b^2 + b - 1 = 1,000 states, so the average of 3,090 is about 3
    times the best case.

    Cyclic slide paths are the biggest bottleneck. A slide can always be undone, so if Black slides 1 to 8, Red
    slides a piece, Black slides 8 back to 1, and Red slides its piece back, the board is the same as it started.
    Unlike the Project 2 search, minimax and alpha-beta have no closed set, so every path to a state is searched
    again even if the same state was already scored somewhere else in the tree. The drop phase has repeats too,
    since dropping on 1 then 2 makes the same board as dropping on 2 then 1, as shown in Table 5.

        Table 5. Repeated States — Leaves Minimax Evaluated vs. Different States
        | Test     | Depth | Leaves Evaluated | Different States | Repeated | Back to the Starting Board |
        |----------|-------|------------------|------------------|----------|----------------------------|
        | drop_1   | 3     | 42,840           | 21,420           | 50.0%    | 0                          |
        | slide_1  | 3     | 6,496            | 3,283            | 49.5%    | 0                          |
        | slide_1  | 4     | 141,855          | 36,072           | 74.6%    | 343                        |
        | slide_11 | 4     | 56,578           | 18,971           | 66.5%    | 179                        |

    At depth 4 on slide_1, 74.6% of the leaves were boards that were already scored somewhere else, and 343 of them
    were the exact starting board, from both players moving a piece and moving it back. So the number of
    different positions grows much slower than b^m, but the search still has to pay for every path.

    The slide phase also has infinite-turn state loops, since nothing ends it except a win and pieces can keep
    sliding back and forth forever (the runner stops a game after 150 turns and calls it a draw). Without a depth
    limit the slide phase game tree is infinite, and plain minimax would never finish since it would keep
    following a cycle like 1 to 8, 8 to 1, 1 to 8, and so on. The depth limit in cutoff_test is what makes the
    search end. This is also why depth 3 is the deepest that can be played, alphabeta at depth 4 takes about 8 to
    9 seconds per move in the drop phase, which is over the runner's 5 second limit, while depth 3 takes about 1.

MOVE EVALUATION
        Table 6. Chosen Move & Score (Minimax vs. Alpha-Beta, depth 3)
        | Test     | Situation                    | Minimax Move | Alpha-Beta Move | Minimax Score | Alpha-Beta Score |
        |----------|------------------------------|--------------|-----------------|---------------|------------------|
        | drop_4   | Black wins, diagonal         | 0 1          | 0 1             | 999,999       | 999,999          |
        | drop_7   | Black wins, horizontal       | 0 16         | 0 16            | 999,999       | 999,999          |
        | drop_8   | Black wins, vertical         | 0 9          | 0 9             | 999,999       | 999,999          |
        | drop_10  | Black wins, 2x2 block        | 0 15         | 0 15            | 999,999       | 999,999          |
        | drop_11  | Black wins, tilted square    | 0 21         | 0 21            | 999,999       | 999,999          |
        | slide_5  | Black wins, vertical         | 13 8         | 13 8            | 999,999       | 999,999          |
        | slide_6  | Red wins, vertical           | 28 29        | 28 29           | 999,999       | 999,999          |
        | slide_8  | Black wins, tilted square    | 34 28        | 34 28           | 999,999       | 999,999          |
        | drop_5   | Black blocks                 | 0 23         | 0 23            | 35            | 35               |
        | drop_12  | Red blocks 2x2 block         | 0 15         | 0 15            | -709          | -709             |
        | slide_3  | Red blocks                   | 16 11        | 16 11           | 26            | 26               |
        | slide_9  | Red blocks tilted square     | 29 28        | 29 28           | -737          | -737             |
        | drop_13  | Black makes a fork           | 0 16         | 0 16            | 999,997       | 999,997          |
        | slide_12 | Black makes a fork           | 7 8          | 7 8             | 999,997       | 999,997          |
        | drop_1   | empty board                  | 0 15         | 0 15            | 69            | 69               |

    Table 6 shows that minimax and alpha-beta pick the exact same move with the exact same score, and this holds
    for every test and depth in benchmark_results.csv. Minimax looks at every state, so alpha-beta matching it on
    all 84 runs shows that pruning only skips states that couldn't change the answer, which is what the Chapter 6
    slides say about alpha-beta not affecting the final result. The win tests find the winning move at every
    depth, including all 6 win shapes and both phases, and drop_8 and slide_5 give 0 9 and 13 8, which are the
    example moves in the assignment.

    The block and fork tests show how depth changes the plan. In drop_5 at depth 1 Black only sees its own move
    and picks 0 8 for the best shape potential, but from depth 2 on it sees Red's reply and blocks with 0 23
    (slide_3 and drop_12 do the same, picking 26 21 and 0 29 at depth 1). The negative scores in drop_12 and
    slide_9 mean Red stopped the win but Black still has the better board. Forks need depth 3, since the search
    has to see the move, the block, and then the other winning square. In drop_13, 0 16 makes 14, 15, 16 with
    both ends open and scores 999,997, a win in 3 moves. In slide_12 depths 1 and 2 pick 23 16, which also makes
    a fork, and depth 3 finds 7 8, which also forces a win in 3 and comes first in the sorted order, so the tie
    goes to the lowest move. The empty board (drop_1) shows the tie-breaking too, since the 4 middle squares all
    score the same and 0 15 is the lowest numbered one, so the same state always gives the same move.