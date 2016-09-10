Solution (scroll all the way down for problem clarification):
First for the double-out part. This is straightforward; one tricky aspect was that I wanted to give good advice as well as correct advice, so when I need to score, say, 20 points, I report that as 'D10' when it is the last, double-out dart, and as 'S20' when it is not, because the 'S20' target is bigger and easier to hit.
from collections import defaultdict

singles = range(1, 21) + [25]
points = set(m*s for s in singles for m in (1,2,3) if m*s != 75)
doubles = set(2*s for s in singles)
ordered_points = [0] + sorted(points, reverse=True)

def double_out(total):
    """Return a shortest possible list of targets that add to total,
    where the length <= 3 and the final element is a double.
    If there is no solution, return None."""
    if total > 60 + 60 + 50:
        return None
    for dart1 in ordered_points:
        for dart2 in ordered_points:
            dart3 = total - dart1 - dart2
            if dart3 in doubles:
                solution = [name(dart1), name(dart2), name(dart3, 'D')]
                return [t for t in solution if t != 'OFF']
    return None

def name(d, double=False):
    """Given an int, d, return the name of a target that scores d.
    If double is true, the name must start with 'D', otherwise,
    prefer the order 'S', then 'T', then 'D'."""
    return ('OFF' if d == 0 else
            'DB' if d == 50 else
            'SB' if d == 25 else
            'D'+str(d//2) if (d in doubles and double) else
            'S'+str(d) if d in singles else
            'T'+str(d//3) if (d % 3 == 0) else
            'D'+str(d//2))
Here is a test suite to go with this:
def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])
    for total in range(2, 159) + [160, 161, 164, 167, 170]:
        assert valid_out(double_out(total), total)
    for total in [0, 1, 159, 162, 163, 165, 166, 168, 169, 171, 200]:
        assert double_out(total) == None

def valid_out(darts, total):
    "Does this list of targets achieve the total, and end with a double?"
    return (0 < len(darts) <= 3 and darts[-1].startswith('D')
            and sum(map(value, darts)) == total)

def value(target):
    "The numeric value of a target."
    if target == 'OFF': return 0
    ring, section = target[0], target[1:]
    r = 'OSDT'.index(target[0])
    s = 25 if section == 'B' else int(section)
    return r * s
Now to find the outcome for each target, and the best target:
def best_target(miss):
    "Return the target that maximizes the expected score."
    return max(targets, key=lambda t: expected_value(t, miss))

def expected_value(target, miss):
    "The expected score of aiming at target with a given miss ratio."
    return sum(value(t)*p for (t, p) in outcome(target, miss).items())

def outcome(target, miss):
    "Return a probability distribution of [(target, probability)] pairs."
    results = defaultdict(float)
    for (ring, ringP) in ring_outcome(target, miss):
        for (sect, sectP) in section_outcome(target, miss):
            if ring == 'S' and sect.endswith('B'):
                # If sect hits bull, but ring misses out to S ring,
                # then spread the results over all sections.
                for s in sections:
                    results[Target(ring, s)] += (ringP * sectP) / 20.
            else:
                results[Target(ring, sect)] += (ringP * sectP)
    return dict(results)

def ring_outcome(target, miss):
    "Return a probability distribution of [(ring, probability)] pairs."
    hit = 1.0 - miss
    r = target[0]
    if target == 'DB': # misses tripled; can miss to SB or to S
        miss = min(3*miss, 1.)
        hit = 1. - miss
        return [('DB', hit), ('SB', miss/3.), ('S', 2./3.*miss)]
    elif target == 'SB': # Bull can miss in either S or DB direction
        return [('SB', hit), ('DB', miss/4.), ('S', 3/4.*miss)]
    elif r == 'S': # miss ratio cut to miss/5
        return [(r, 1.0 - miss/5.), ('D', miss/10.), ('T', miss/10.)]
    elif r == 'D': # Double can miss either on board or off
        return [(r, hit), ('S', miss/2), ('OFF', miss/2)]
    elif r == 'T': # Triple can miss in either direction, but both are S
        return [(r, hit), ('S', miss)]

def section_outcome(target, miss):
    "Return a probability distribution of [(section, probability)] pairs."
    hit = 1.0 - miss
    if target in ('SB', 'DB'):
        misses = [(s, miss/20.) for s in sections]
    else:
        i = sections.index(target[1:])
        misses = [(sections[i-1], miss/2), (sections[(i+1)%20], miss/2)]
    return  [(target[1:], hit)] + misses

def Target(ring, section):
    "Construct a target name from a ring and section."
    if ring == 'OFF':
        return 'OFF'
    elif ring in ('SB', 'DB'):
        return ring if (section == 'B') else ('S' + section)
    else:
        return ring + section

sections = "20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split()
targets = set(r+s for r in 'SDT' for s in sections) | set(['SB', 'DB'])
Again, a test suite:
def test_darts2():
    assert best_target(0.0) == 'T20'
    assert best_target(0.1) == 'T20'
    assert best_target(0.4) == 'T19'
    assert same_outcome(outcome('T20', 0.0), {'T20': 1.0})
    assert same_outcome(outcome('T20', 0.1), 
                        {'T20': 0.81, 'S1': 0.005, 'T5': 0.045, 
                         'S5': 0.005, 'T1': 0.045, 'S20': 0.09})
    assert same_outcome(
            outcome('SB', 0.2),
            {'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016,
             'DB': 0.04, 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016,
             'S19': 0.016, 'S18': 0.016, 'S13': 0.016, 'S12': 0.016,
             'S11': 0.016, 'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 'S15':
             0.016, 'S14': 0.016, 'S7': 0.016, 'SB': 0.64})
    assert same_outcome(outcome('T20', 0.3),
                        {'S1': 0.045, 'T5': 0.105, 'S5': 0.045,
                         'T1': 0.105, 'S20': 0.21, 'T20': 0.49})
    assert best_target(0.6) == 'T7'
Clarifications:
Let me try to clarify a bit more. My apologies for any confusion. The key is to note thathere are two independent ways to miss, by ring and by section. One way to implement this idea is to have separate functions to return probability distributions for ring and section outcomes. But whether you have separate functions or not, mathematically you need to obey the independence equation:
P(Ring, Section) = P(Ring) * P(Section)
A note on notation: the target names are given in the problem: 'S1' to 'S20', 'D1' to 'D20', 'T1' to 'T20', along with 'SB', 'DB', and 'OFF'. But names for rings and sections are not given. In this explanation I will name the rings 'S', 'D' and 'T' for single/double/triple, along with 'OFF', 'SB' and 'DB'. I will name the sections '1' to '20', along with 'B' (encompassing the whole bulls-eye section, SB and DB).
For example, consider aiming for the S20 target with a miss ratio of 0.2. "If you aim for a thick single ring, it is about 5 times thicker than the thin rings, so your miss ratio is reduced to 1/5th [of your given miss rate; in this case from 0.2 to 0.04], and of these, half go to the double ring and half to the triple", so we have:
>>> ring_outcome('S20', .2)
{'S': 0.96, 'D': 0.02, 'T': 0.02}
For the section outcome, 1/2 the misses go clockwise to the 1 and half counterclockwise to the 5 and we get:
>>> section_outcome('S20', .2)
{'1': 0.1, '5': 0.1, '20': 0.8}
These Ring and Section outcomes are independent, so combining them we get:
>>> outcome('S20', .2)
{'D20': 0.016, 'S1': 0.096, 'T5': 0.002, 'S5': 0.096, 'T1': 0.002, 
 'S20': 0.768, 'T20': 0.016, 'D5': 0.002, 'D1': 0.002}
Most of the discussion centers (ha ha) on the bulls-eye. According to the definition of ring accuracy for the single bull, "If you aim for the single bull, 1/4 of your [ring] misses go to the double bull and 3/4 to the single ring." So that gives us:
>>> ring_outcome('SB', .2)
{'SB': 0.8, 'S': 0.15, 'DB': 0.05}
For the section outcome, a miss goes equally to each of the 20 non-bull sections:
>>> section_outcome('SB', .2)
{'B': 0.8, '11': 0.01, '10': 0.01, '13': 0.01, '20': 0.01, '14': 0.01, '17': 0.01, 
 '16': 0.01, '19': 0.01, '18': 0.01, '1': 0.01, '3': 0.01, '2': 0.01, '5': 0.01, 
 '4': 0.01, '7': 0.01, '6': 0.01, '9': 0.01, '15': 0.01, '12': 0.01, '8': 0.01}
Make sure that you can duplicate these results (whether you explicitly have separate ring_outcome and section_outcome function, or whether you have the calculations combined into one function).
For most people, the confusion comes in combining these. Some of the combinations are easy. Again, these are independent, so combining the ring outcome {'SB': 0.8} with the section outcome {'B': 0.8} clearly results in {'SB': 0.64}. And combining two misses, like ring outcome {'S': 0.15} with section outcome {'11': 0.01} yields {'S11': 0.0015}.
But the confusing part, to some people, is what happens when you combine the ring outcome {'S': 0.15} with the section outcome {'B': 0.8}? The probability is 0.12, but where does it go? The answer is "If you aim for the bull and miss on rings, then the section you end up on is equally possible among all 20 sections. But independent of that you can also miss on sections; again such a miss is equally likely to go to any section and should be recorded as being in the single ring." So this gives you 0.12/20 = 0.006 for each of 'S1' through 'S20'. So the final total for each of 'S1' through 'S20' is 0.01 + 0.006 = 0.016, and we get this:
>>> outcome('SB', .2)
{'S9': 0.016, 'S8': 0.016, 'S3': 0.016, 'S2': 0.016, 'S1': 0.016, 'DB': 0.04, 
 'S6': 0.016, 'S5': 0.016, 'S4': 0.016, 'S20': 0.016, 'S19': 0.016, 'S18': 0.016, 
 'S13': 0.016, 'S12': 0.016, 'S11': 0.016, 'S10': 0.016, 'S17': 0.016, 'S16': 0.016, 
 'S15': 0.016, 'S14': 0.016, 'S7': 0.016, 'SB': 0.64}
We decided that the grading program will be lenient: because we had some erroneous/confusing statements the first day the exam was out, we will also allow the interpretation that {'S': 0.15} and {'B': 0.8} combine to {'SB': 0.12}. That would give you:
>>> outcome('SB', .2)
{'S9': 0.01, 'S8': 0.01, 'S3': 0.01, 'S2': 0.01, 'S1': 0.01, 'DB': 0.04, 'S6': 0.01, 
 'S5': 0.01, 'S4': 0.01, 'S19': 0.01, 'S18': 0.01, 'S13': 0.01, 'S12': 0.01, 'S11': 0.01,
 'S10': 0.01, 'S17': 0.01, 'S16': 0.01, 'S15': 0.01, 'S14': 0.01, 'S7': 0.01, 'S20': 0.01,
 'SB': 0.76}
Finally, for those who are interested in learning more, consider this page: http://www.stat.cmu.edu/~ryantibs/darts/ Note that the simplified target model I present in this exercise duplicates some of the findings they come up with, particularly in the path of the optimal target as the miss ratio increases.
I made a mistake in saying: "If you aim for the double bull, it is tiny, so your miss rate [for the ring] is tripled." Obviously that statement makes no sense when the miss ratio is greater than 1/3. You should interpret that as "If you aim for the double bull, it is tiny, so your miss rate [for the ring] is tripled, except that a miss rate can never exceed 1.0, so any input miss rate of 1/3 or higher will have a miss rate of 1 for the bull ring."
And finally, to share a status update: last time I checked, 92% of students who submitted an answer to this problem got it right, which is the same percentage as 2 and 4, and a couple percent behind the other problems.
