"""
UNIT 2: Logic Puzzle

You will write code to solve the following logic puzzle:

1. The person who arrived on Wednesday bought the laptop.
2. The programmer is not Wilkes.
3. Of the programmer and the person who bought the droid,
   one is Wilkes and the other is Hamming.
4. The writer is not Minsky.
5. Neither Knuth nor the person who bought the tablet is the manager.
6. Knuth arrived the day after Simon.
7. The person who arrived on Thursday is not the designer.
8. The person who arrived on Friday didn't buy the tablet.
9. The designer didn't buy the droid.
10. Knuth arrived the day after the manager.
11. Of the person who bought the laptop and Wilkes,
    one arrived on Monday and the other is the writer.
12. Either the person who bought the iphone or the person who bought the tablet
    arrived on Tuesday.

You will write the function logic_puzzle(), which should return a list of the
names of the people in the order in which they arrive. For example, if they
happen to arrive in alphabetical order, Hamming on Monday, Knuth on Tuesday, etc.,
then you would return:

['Hamming', 'Knuth', 'Minsky', 'Simon', 'Wilkes']

(You can assume that the days mentioned are all in the same week.)
"""


def logic_puzzle():
    "Return a list of the names of the people, in the order they arrive."
    ## your code here; you are free to define additional functions if needed
    ## The only non-trivial part is arithmetic over days, so I decided to
    ## base my representation on days: 1 for Monday, 2 for Tuesday, etc.,
    ## and have each attribute (name, profession, purchase) take on the
    ## value of a day.  The rest is easy, except that I have to recover the
    ## names in the proper order.  I do that by putting Name=daynumber pairs
    ## in a dict, and having the function answer sort them into order.
    days = (mon, tue, wed, thu, fri) = (1, 2, 3, 4, 5)
    possible_days = list(permutations(days))
    return next(answer(Wilkes=Wilkes, Hamming=Hamming, Minsky=Minsky,
                       Knuth=Knuth, Simon=Simon)
                for (Wilkes, Hamming, Minsky, Knuth, Simon) in possible_days
                if Knuth == Simon + 1 # 6
                for (programmer, writer, manager, designer, _) in possible_days
                if Knuth == manager + 1 # 10
                if thu != designer # 7
                if programmer != Wilkes and writer != Minsky # 2, 4
                for (laptop, droid, tablet, iphone, _) in possible_days
                if set([laptop, Wilkes]) == set([mon, writer]) # 11
                if set([programmer, droid]) == set([Wilkes, Hamming]) # 3
                if iphone == tue or tablet == tue # 12
                if designer != droid # 9
                if Knuth != manager and tablet != manager # 5
                if wed == laptop # 1
                if fri != tablet # 8
                )

from itertools import permutations

def answer(**names):
    "Given a dict of {name:day_of_week}, return a list of names sorted by day."
    return sorted(names, key=lambda name: names[name])

print logic_puzzle()

