# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def name(s):
    rs = xrange(1,21)
    rsn = map(lambda x: (x, 'S'+str(x)), rs)
    dsn = map(lambda x: (x*2, 'D'+str(x)), rs)
    tsn = map(lambda x: (x*3, 'T'+str(x)), rs)
    # rsn tsn dsn order matters for problem statement!
    score_list = rsn + tsn + dsn + [(25, 'SB'), (50, 'DB')]
    scores = {}
    for item in score_list:
        try:
            scores[item[0]] += [item[1]]
        except:
            scores[item[0]] = [item[1]]
    return scores[s]

def make_points(version="all"):
    op = set([25,50])
    r = xrange(1,21)
    if version == "all":
        for i in [1,2,3]: 
	    op = op.union(set(map(lambda x: x*i, r)))
    if version == "double":
        op = op.union(set(map(lambda x: x*2, r)))
    return [0] + list(reversed(list(op)))

def target(s):
    points = make_points()
    double = make_points("double")
    for dart1 in points:
        if dart1 == s: return [dart1]
        for dart2 in points:
            if dart1 + dart2 == s: return [dart1, dart2]
            for dart3 in double:
                if dart1 + dart2 + dart3 == s: return [dart1, dart2, dart3]
    return None
  
def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
#    print double_out(146), (["T20", "T18", "D16"], ["T19", "T19", "D16"])
#    print double_out(23)
#    print double_out(19)
#    print double_out(18)
#    print double_out(0)
    print 'tests pass'

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""

#{1: ['S1'], 2: ['S2', 'D1'], 3: ['S3', 'T1'], 4: ['S4', 'D2'], 5: ['S5'], 6: ['S6', 'T2', 'D3'], 7: ['S7'], 8: ['S8', 'D4'], 9: ['S9', 'T3'], 10: ['S10', 'D5'], 11: ['S11'], 12: ['S12', 'T4', 'D6'], 13: ['S13'], 14: ['S14', 'D7'], 15: ['S15', 'T5'], 16: ['S16', 'D8'], 17: ['S17'], 18: ['S18', 'T6', 'D9'], 19: ['S19'], 20: ['S20', 'D10'], 21: ['T7'], 22: ['D11'], 24: ['T8', 'D12'], 25: ['SB'], 26: ['D13'], 27: ['T9'], 28: ['D14'], 30: ['T10', 'D15'], 32: ['D16'], 33: ['T11'], 34: ['D17'], 36: ['T12', 'D18'], 38: ['D19'], 39: ['T13'], 40: ['D20'], 42: ['T14'], 45: ['T15'], 48: ['T16'], 50: ['DB'], 51: ['T17'], 54: ['T18'], 57: ['T19'], 60: ['T20']}


def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    def _choose(score, position, length):
        if position == length-1:
            return name(score)[-1]  # get me a double
        return name(score)[0] # easy one first
    points = target(total)
    if points:
        s_points = filter(lambda x: x != 0, points)
        length = len(s_points)
        if length:
            r = [ _choose(j, i, length) for i, j in enumerate(s_points)]
            if ((r[-1][0] is "S") and (r[-1] is not "SB")) or (r[-1][0] is "T"):
                return None
            else:
                return r
    return None

test_darts()

"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""

def ringmiss(miss, ring):
    dbmiss = miss*3 if miss*3 < 1 else 1
    if ring == "T":  return {"T": 1-miss, "S": miss}
    if ring == "D":  return {"D": 1-miss, "S": miss*0.5, "OFF": miss*0.5}
    if ring == "S":  return {"S": 1-(miss*0.2), "D": miss*0.1, "T": miss*0.1}
    if ring == "SB": return {"SB": 1-miss, "DB": miss*0.25, "S": miss*0.75}
    if ring == "DB": return {"DB": (1-miss)/3.,"S": (1-((1-miss)/3.))*2/3., "SB": (1-((1-miss)/3.))*1/3.}

    
def sectionmiss(miss, section):
    cw = "20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split()
    def _neighbar():
        for i, j in enumerate(cw):
            if j == section:
                right = cw[0] if i == 19 else cw[i+1]
                left = cw[19] if i == 0 else cw[i-1]
        return left, right
    left, right = _neighbar()
    return {section: 1-miss, left: miss/2, right: miss/2}


def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    if target == "SB" or target == "DB":
        ring = ringmiss(miss, target)
    else:
        ring = ringmiss(miss, target[0])
        section = sectionmiss(miss, target[1:]) 

    prob = {}

    if target in ["SB", "DB"]:
        switch = {"SB": "DB", "DB": "SB"}
        bull1 = ring[target]
        bull2 = ring[switch[target]]
        prob = {target: bull1*bull1, switch[target]: bull1*bull2}
        single = (1 - prob[target] - prob[switch[target]])/20
        for i in range(1,21):
            prob["S"+str(i)] = single 
    else:
        for (rx, ry) in ring.items():
            for (sx, sy) in section.items():
                if (ry*sy) and (rx == "OFF"):
                    try: prob[rx] += ry*sy
                    except: prob[rx] = ry*sy
                elif (ry*sy): prob[rx+sx] = ry*sy
    return prob

def check(d):
    return sum([j for i, j in d.items()])

def check_outcome():   
    for i in "S D T".split():
        for j in "20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split():
            for m in map(lambda x: x/10. ,range(0,10)):
               if not check(outcome("%s" % i+j, m)) - 1 <= 0.00001:
                   print "Error: ",  i+j
    return "OK"


def score(x):
    if x == "SB": return 25
    elif x == "DB": return 50
    elif x[0] == "S": return int(x[1:])
    elif x[0] == "D": return int(x[1:])*2
    elif x[0] == "T": return int(x[1:])*3
    elif x == "OFF": return 0

def best(out):
    result = []
    for (x,y) in out.items():
        result.append(score(x)*y)
    return sum(result)


def best_target(miss):
    "Return the target that maximizes the expected score."
    values = []
    targets = make_points()
    for i in targets[1:]:
        n = name(i)[0]
        out = outcome(n, miss)
        values.append((best(out), n))
    return max(values, key=lambda (x, y): x)[1]

print best_target(0.5)

       
def same_outcome(dict1, dict2):
    "Two states are the same if all corresponding sets of locs are the same."
    return all(abs(dict1.get(key, 0) - dict2.get(key, 0)) <= 0.0001
               for key in set(dict1) | set(dict2))

def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert (same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016, 'S11': 0.016,
             'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15': 0.016, 'S14': 0.016,
             'S7': 0.016, 'SB': 0.64}))

test_darts2()
