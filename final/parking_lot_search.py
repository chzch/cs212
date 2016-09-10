"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(start, successors, is_goal)

    
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple(range(start,start+n*incr,incr))

    
def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    walls = sorted(range(0,N) + range(N,N*N-N,N) + range(N*2-1,N*N-N,N) + range(N*N-N,N*N))
    walls2 = ('|', tuple(filter(lambda x: x != (N*N-1)/2, walls)))
    return (('@', ((N*N-1)/2,)),) + cars + (walls2,)


def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))



def is_goal(state):
    "A move is a tuple consisting of (object, location)"
    for (obj, loc) in state:
        if obj == "@":
            goal = loc[0]
    for (obj, loc) in state:
        if obj == "*":
            if goal in loc:
                return True
    return False

def ori(obj):
    "V - vertical and H - horizontal"
    return "H" if locs(obj[1][0],len(obj[1])) == obj[1] else "V"
 



#############################
def move_car(obj, state, d):
    """d indicates is the direction the car wants to move to
    when the move is possible --> (object, location) 
    when not possible --> None"""
    if ori(obj) == "H":
        if d == "r": 
            goal = obj[1][-1] + 1
            move = 1
            new_locs = locs(obj[1][0] + 1, len(obj[1]))
        elif d == "l": 
            goal = obj[1][0] - 1
            move = -1
            new_locs = locs(obj[1][0] - 1, len(obj[1]))
        else: return None, None

    if ori(obj) == "V":
        if d == "u": 
            goal = obj[1][0] - N
            move = - N
            new_locs = locs(obj[1][0] - N, len(obj[1]), N)
        elif d == "d": 
            goal = obj[1][-1] + N
            move = + N
            new_locs = locs(obj[1][0] + N, len(obj[1]), N)
        else: return None, None

    for (obst, loc) in state:
        if (obst is not obj) and (obst is not '@') and (goal in loc):
            return None, None

    new_state = grid(tuple([(i,j) if i != obj[0] else (obj[0], new_locs) for (i, j) in state]))
    return (new_state, (obj[0], move))
############################





def search_cars(k, i, state):
    for (obst, loc) in state:
        if (i in loc) and (k != obst) and (obst != "@"):
            return False
#    print k, i
    return True    

def move_right(obj, state):
    i = obj[1][-1]
    j = 0
    while search_cars(obj[0], i, state):
        i += 1
        j += 1
    return locs(obj[1][0]+j-1, len(obj[1])), j-1

def move_left(obj, state):
    i = obj[1][0]
    j = 0
    while search_cars(obj[0], i, state):
        i -= 1
        j -= 1
    return locs(obj[1][0]+j+1, len(obj[1])), j+1

def move_up(obj, state):
    i = obj[1][0]
    j = 0
    while search_cars(obj[0], i, state):
        i -= N
        j -= N
    return locs(obj[1][0]+j+N, len(obj[1]), N), j+N

def move_down(obj, state):
    i = obj[1][-1]
    j = 0
    while search_cars(obj[0], i, state):
        i += N
        j += N
    return locs(obj[1][0]+j-N, len(obj[1]), N), j-N


def move_car2(obj, state, d):
    move = 0
    if ori(obj) == "H":
        if d == "r": new_locs, move = move_right(obj, state)
        elif d == "l": new_locs, move = move_left(obj, state)
        else: return None, None
    if ori(obj) == "V":
        if d == "u": new_locs, move = move_up(obj, state)
        elif d == "d": new_locs, move = move_down(obj, state)
        else: None, None
    if move == 0: return None, None
    new_state = grid(tuple([(i,j) if i != obj[0] else (obj[0], new_locs) for (i, j) in state]))
    return (new_state, (obj[0], move))
    
def successors(state):
    """gives back a list [state, (object, action), state, ( ... ) ] for 
    all possible moves for all obj on the parking lot"""
    result = []
    for obj in state:
        if (obj[0] is not "|") and (obj[0] is not "@"):
            u = move_car2(obj, state, "u")
            d = move_car2(obj, state, "d")
            r = move_car2(obj, state, "r")
            l = move_car2(obj, state, "l")
            if u[0]: result.append(u)
            if d[0]: result.append(d)
            if r[0]: result.append(r)
            if l[0]: result.append(l)
    return result

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s):
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]




##############################################################################


import os
import time
from itertools import cycle

cars = cycle('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
hcar = lambda start, l=2: (next(cars), locs(start, l))
vcar = lambda start, l=2: (next(cars), locs(start, l, N))
star = lambda start: ('*', locs(start, 2))

sp = grid((
    hcar( 9, 3), vcar(12, 2), vcar(13, 3), vcar(17, 2), hcar(18, 2),
    star(27),
    hcar(33, 2), vcar(35, 2), vcar(38, 2), vcar(42, 2), hcar(44, 2), hcar(51, 2), hcar(53, 2),
    ))

def animate_puzzle(puzzle, N=8):
    "Shows a puzzle being solved step by step"
    state = dict(puzzle)
    for car, moveby in path_actions(solve_parking_puzzle(puzzle, N)):
        start = min(state[car])
        steps = abs(moveby if abs(moveby) < N else moveby / N)
        step = moveby / steps
        for i in range(1, steps+1):
            state[car] = locs(start + i*step, len(state[car]), abs(step))
            os.system('cls' if os.name=='nt' else 'clear')
            show(state.items())
            time.sleep(0.7)

animate_puzzle(sp)


def my_tests():
    #show(puzzle1)
    obj1 = ('*', (26, 27))
    obj2 = ('B', (20, 28, 36))
    obj3 = ('G', (9, 10))
    assert move_car(obj1, puzzle1, "r") == (None, None)
    assert move_car(obj1, puzzle1, "l") == (None, None)
    assert move_car(obj1, puzzle1, "u") == (None, None)
    assert move_car(obj1, puzzle1, "d") == (None, None)
    assert move_car(obj2, puzzle1, "r") == (None, None)
    assert move_car(obj2, puzzle1, "l") == (None, None)
    s1, a1 = move_car(obj2, puzzle1, "u")
    #show(s1)
    #assert a1 == ('B', (12, 20, 28))
    #print '--------------------------------' 
    #show(puzzle1)
    s2, a2 =  move_car(obj2, puzzle1, "d")
    #show(s2)
    #assert a2 == ('B', (28, 36, 44))
    #print '--------------------------------'
    #show(puzzle1)
    s3, a3 = move_car(obj3, puzzle1, "r")
    #show(s3)
    #assert a3 == ('G', (10, 11))
    assert move_car(obj3, puzzle1, "l") == (None, None)
    assert move_car(obj3, puzzle1, "u") == (None, None)
    assert move_car(obj3, puzzle1, "d") == (None, None)

    show(puzzle1)
    obj8 = ('A', (45, 46))
    print move_right(obj3, puzzle1)
    print move_left(obj8, puzzle1)
    print move_up(obj2, puzzle1)

    #print successors(puzzle1)

    assert is_goal(puzzle1) == False
    puzzle4 = grid((
    ('*', locs(30, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))
    assert is_goal(puzzle4) == True

    final_path = shortest_path_search(puzzle1, successors, is_goal)
    for i in final_path[0::2]:
        show(i)
    print path_actions(final_path)

    print path_actions(shortest_path_search(puzzle2, successors, is_goal))
    print path_actions(shortest_path_search(puzzle3, successors, is_goal))

    print path_actions(solve_parking_puzzle(puzzle1))


#my_tests()
