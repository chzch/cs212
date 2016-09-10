from functools import update_wrapper


#def find_anagrams(list_of_w, list_of_wc, list_of_sol, shortest):
#    while list_of_w:
#        collect_words(list_of_wc, list_of_w, shortest)
#        apply_words(list_of_sol, list_of_w, list_of_wc, phrase)
#        print len(list_of_w)


    
def apply_words(list_of_sol, list_of_w, list_of_wc, phrase):
    while list_of_wc:
        word = list_of_wc[0]
        for w in word[2]:
            new_phrase = sort_string(removed(word[0], w))
            new_word = (new_phrase, word[1] | frozenset([w]), set([]))
            if is_solution(phrase, new_word) and new_word not in list_of_sol:
                list_of_sol.append(new_word)
            if is_valid(new_word):
                list_of_w.append(new_word)
        list_of_wc.pop(0)

def collect_words(list_of_wc, list_of_w, shortest):
    test = lambda x: len(x) >= shortest
    while list_of_w:
        word = list_of_w[0]
        first = word[0]
        if first:
            second = word[1]
            third = filter(test, find_words(first))
            list_of_wc.append((first, second, third))
        list_of_w.pop(0)
            
def is_valid(word):
    return word[0] is not ''

def is_solution(phrase, word):
    return phrase == sort_string(''.join(word[1]))

def sort_string(string):
    return ''.join(sorted(string))



def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

#########

@memo
def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

@memo
def find_words(letters):
    return extend_prefix('', letters, set())

def extend_prefix(pre, letters, results):
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            extend_prefix(pre+L, letters.replace(L, '', 1), results)
    return results

def prefixes(word):
    "A list of the initial sequences of a word, not including the complete word."
    return [word[:i] for i in range(len(word))]

def readwordlist(filename):
    "Return a pair of sets: all the words in a file, and all the prefixes. (Uppercased.)"
    wordset = set(open(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset

WORDS, PREFIXES = readwordlist('words4k.txt')

###############
#TESTS
###############

phrase = sort_string('TOOTHBRUSH')
t_word = (phrase, frozenset([]), set([]))

t_list_of_wc = []
t_list_of_w = [t_word]
t_list_of_sol = []


while t_list_of_w:
    collect_words(t_list_of_wc, t_list_of_w, 2) 
    apply_words(t_list_of_sol, t_list_of_w, t_list_of_wc, phrase)
    print "t_list_of_wc  ", len(t_list_of_wc)
    print "t_list_of_w   ", len(t_list_of_w)
    print "t_list_of_sol ", len(t_list_of_sol)

#find_anagrams(t_list_of_w, t_list_of_wc, t_list_of_sol, "2")

print t_list_of_sol
