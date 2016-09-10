### version with list comprehension

def find_water_zebra():
    import itertools

    houses = [first, _, middle, _, _] = [1,2,3,4,5]

    orderings = list(itertools.permutations(houses)) #1

    def imright(h1,h2):
        "House h1 is immediately right of h2 if h1=h2 = 1"
        return h1-h2 == 1
        
    def nextto(h1,h2):
        "Two houses are next to each other if they differ by 1"
        return abs(h1-h2) == 1

    return [result for result in (
            (   ('Drinks',  {'coffee':coffee,'tea':tea,'milk':milk,'WATER':WATER,'oj':oj}),
                ('Nations', {'Englishman':Englishman, 'Spaniard':Spaniard, 
                               'Ukranian':Ukranian, 'Japanese':Japanese, 'Norwegian':Norwegian}),
                ('Colours', {'red':red, 'green':green, 'ivory':ivory, 'yellow':yellow, 'blue':blue}),
                ('Pets',    {'dog':dog, 'snails':snails, 'fox':fox, 'horse':horse, 'ZEBRA':ZEBRA}),
                ('Smokes',  {'OldGold':OldGold, 'Kools':Kools, 'Chesterfields':Chesterfields, 
                                'LuckyStrike':LuckyStrike, 'Parliaments':Parliaments}),
            )

            for (red, green, ivory, yellow, blue) in orderings
            if imright(green, ivory)        #6
            for (Englishman, Spaniard, Ukranian, Japanese, Norwegian) in orderings
            if Englishman is red            #2 
            if Norwegian is first           #10
            if nextto(Norwegian, blue)      #15
            for (coffee, tea, milk, oj, WATER) in orderings
            if coffee is green              #4
            if Ukranian is tea              #5
            if milk is middle               #9
            for (OldGold, Kools, Chesterfields, LuckyStrike, Parliaments) in orderings
            if Kools is yellow              #8
            if LuckyStrike is oj            #13
            if Japanese is Parliaments      #14
            for (dog, snails, fox, horse, ZEBRA) in orderings
            if Spaniard is dog              #3
            if OldGold is snails            #7
            if nextto(Kools, horse)         #12
            if nextto(Chesterfields, fox)   #11
            )
        ]    

hps = find_water_zebra()
print 'Result count:',len(hps)
if len(hps) < 20:
    for hp in hps:
        print 'House ',''.join('%15s'%(num if num else 'House') for num in range(1,6))    
        for item, props in hp:
            propKeys = sorted(props.keys(),key=lambda k:props[k]) # sort on props[k]: house 
            print '%-7s'%item, ''.join(['%15s'%propKey for propKey in propKeys])
        print
