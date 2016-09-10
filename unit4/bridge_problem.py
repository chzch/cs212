def bridge_problem(here):
    here = frozenset(here) | frozenset(['light'])
    explored = set() # set of states we have visited
    # state will be a (people-here, people-there, time-elapsed)
    frontier = [ [(here, frozenset(), 0)] ] # ordered list of pattern
    if not here:
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        here1, there1, t1 = state1 = path[-1]
        if not here1 or here1 == set(['light']): #Check for solution when we pull best path off
            return path
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                here, there, t = state
                explored.add(state)
                path2 = path + [action, state]
                #Don't check for solution when we extend a path
                frontier.append(path2)
                frontier.sort(key=elapsed_time)
    return []


def elapsed_time(path):
    return path[-1][2]

def bsuccessors(state):
    here, there, t = state
    if 'light' in here:
        return dict(((here - frozenset([a,b, 'light']),
                     there | frozenset([a,b, 'light']),
                     t + max(a,b)),
                     (a,b, '->'))
                     for a in here if a is not 'light'
                     for b in here if b is not 'light')
    else:
        return dict(((here | frozenset([a,b, 'light']),
                     there - frozenset([a,b, 'light']),
                     t + max(a,b)),
                     (a,b,'<-'))
                     for a in there if a is not 'light'
                     for b in there if b is not 'light')



#print bridge_problem([1,2,5,10])
#print bridge_problem([1,2,5,10])[1::2]

print bridge_problem([9,8,7,6,5])[1::2]

