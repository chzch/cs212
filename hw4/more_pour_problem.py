# -----------------
# User Instructions
# 
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes 
# as input capacities, goal, and (optionally) start. This function should 
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the 
# volume of a glass. 
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i), 
# ('empty', i), ('pour', i, j) where i and j are indices indicating the 
# glass number. 

import functools
import itertools

def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    # if no start given default start to all glasses empty
    if not start: start = tuple([0 for _ in range(len(capacities))])
    is_goal = lambda state: goal in state
    d_successors = lambda state: m_successors(state, capacities)
    return shortest_path_search(start, d_successors, is_goal)
        
def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set()
    frontier = [ [start] ] 
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return Fail

Fail = []

def m_successors(state, capacities):
    assert False not in map(lambda x, y: x<=y, state, capacities)
    items = []              
    items += [tuple([ s , ('fill', i) ]) for s, i in fill(state, capacities)]
    items += [tuple([ s , ('empty', i) ]) for s, i in empty(state)]
    items += [tuple([ s , ('pour', i, j)]) for s, i, j in pour(state, capacities)]   
    return dict(items)

def empty(state):
    result = []
    glass = []
    length = len(state)
    i = 0
    j = 0
    while i < length:
        if not state[i] == 0:
            while j < length:
                if i == j:
                    glass.append(0)
                else:
                    glass.append(state[j])
                j += 1
            result += [[tuple(glass), i]]
            glass = []
        i += 1
        j = 0
    return result

def fill(state,capacities):
    result = []
    glass = []
    length = len(state)
    i = 0
    j = 0
    while i < length:
        if not state[i] == capacities[i]:
            while j < length:
                if i == j:
                    glass.append(capacities[i])
                else:
                    glass.append(state[j])
                j += 1
            result += [[tuple(glass), i]]
            glass = []
        i += 1
        j = 0
    return result

def pour(state, capacities):
    space = []
    length = len(state)
    i = 0
    temp = list(state)
    while i < length:
        space.append(capacities[i]-state[i])
        i += 1
    v = zip(state,space)
    result = []
    i = 0
    j = 0
    while i < length:
        while j < length:
            if not i == j:
                if v[i][1] >= v[j][0] and v[j][0] > 0:
                    temp[i] = v[i][0] + v[j][0]
                    temp[j] = 0
                    result.append([tuple(temp),i, j])
                if v[i][1] < v[j][0] and v[i][1] > 0:
                    temp[i] = v[i][1]
                    temp[j] = v[j][0]-v[i][1]
                    result.append([tuple(temp), j, i])      
            j += 1
            temp = list(state)
        i += 1
        j = 0
    return result            


#print 'm_successors((0,0,0,3),(1,2,4,8)) ==> ', m_successors((0,0,0,3),(1,2,4,8))
#print m_successors((0,0,4),(1,2,4))
#def test_successors():
#    assert m_successors((0,0,0,0),(1,2,4,8)) == {(1,0,0,0):('fill',0), (0,2,0,0):('fill',1), (0,0,4,0):('fill',2), (0,0,0,8):('fill',3)}
#    assert m_successors((1,2,4,8,(1,2,4,8)) == {(0,2,4,4):('empty',0), (1,0,4,8):('empty',1), (1,2,0,8):('empty',2), (1,2,4,0):('empty',3)}
#    return 'tests pass'
#print test_successors()
#assert more_pour_problem((1, 2, 4, 8), 4) == [(0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
#print '1 ok'
#print more_pour_problem((1, 2, 4), 3) 
#print "== [(0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]"
    


def test_more_pour():
    assert more_pour_problem((1, 2, 4, 8), 4) == [
        (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
    assert more_pour_problem((1, 2, 4), 3) == [
        (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)] 
    starbucks = (8, 12, 16, 20, 24)
    assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
    assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
    assert more_pour_problem((1, 3, 9, 27), 28) == []
    return 'test_more_pour passes'

print test_more_pour()
