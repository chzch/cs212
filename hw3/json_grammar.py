from string import split


def grammar(description, whitespace=r'\s*'):
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

JSON = grammar("""
string => chars
chars  => char chars | char
""", whitespace='()')


def verify(G):
    lhstokens = set(G) - set([' '])
    rhstokens = set(t for alts in G.values() for alt in alts for t in alt)
    def show(title, tokens): print title,'=',' '.join(sorted(tokens))
    show('Non-Terms', G)
    show('Terminals', rhstokens - lhstokens)
    show('Suspects ', [t for t in (rhstokens - lhstokens) if t.isalnum()])
    show('Orphans  ', lhstokens - rhstokens)



verify(JSON)
