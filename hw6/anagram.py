# -----------------
# User Instructions
# 
# This homework deals with anagrams. An anagram is a rearrangement 
# of the letters in a word to form one or more new words. 
#
# Your job is to write a function anagrams(), which takes as input 
# a phrase and an optional argument, shortest, which is an integer 
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams. 
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that 
# your function returns should include 'AN ARM SAG', but should NOT 
# include 'ARM SAG AN', or 'SAG AN ARM', etc...

import functools

def anagrams(phrase, shortest=2):
    """Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words 
    have length >= shortest. Phrases in answer must have words in 
    lexicographic order (not all permutations)."""
    phrase2 = ''.join(phrase.split())
    words = collect([ phrase2, [], [] ], shortest)
    new = remove_letters(words, shortest)

    def find_anagram(data, result):
        if data == []:
            return result
        else:
            a_list, r_list = [], []
            word_fn = functools.partial(word_in_word, phrase2)
            result += filter(word_fn, data)

            data2 = filter(lambda x: x[0] is not '', data)
            for p in data2:
                collection = collect(p, shortest)
	        if (collection[0] >= shortest) and collection[2]:
                    a_list.append(collect(p, shortest))
            for a in a_list:
                r = remove_letters(a, shortest)
                r_list = r_list + r

        return find_anagram(r_list, result)

    return set([' '.join(sorted(entry[1])) for entry in find_anagram(new, [])])
               
def word_in_word(phrase, data):
    return ''.join(sorted(''.join(data[1]))) == ''.join(sorted(phrase))

def collect(word, shortest):
    return word[:-1] + [filter(lambda x: len(x) >= shortest, find_words(word[0]))]         
    
def remove_letters(wl, shortest):
    new_wl = []
    for word in wl[-1]:
        new_wl.append([removed(wl[0], word), wl[1] + [word], []])
    return new_wl


# ------------
# Helpful functions
# 
# You may find the following functions useful. These functions
# are identical to those we defined in lecture. 

def removed(letters, remove):
    "Return a str of letters, but with each letter in remove removed once."
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

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

# ------------
# Testing
# 
# Run the function test() to see if your function behaves as expected.



def test():
    assert 'DOCTOR WHO' in anagrams('TORCHWOOD')
    assert 'BOOK SEC TRY' in anagrams('OCTOBER SKY')
    assert 'SEE THEY' in anagrams('THE EYES')
    assert 'LIVES' in anagrams('ELVIS')
    assert anagrams('PYTHONIC') == set([
        'NTH PIC YO', 'NTH OY PIC', 'ON PIC THY', 'NO PIC THY', 'COY IN PHT',
        'ICY NO PHT', 'ICY ON PHT', 'ICY NTH OP', 'COP IN THY', 'HYP ON TIC',
        'CON PI THY', 'HYP NO TIC', 'COY NTH PI', 'CON HYP IT', 'COT HYP IN',
        'CON HYP TI'])
    return 'tests pass'

#print test()

print anagrams('TORCHWOOD')
