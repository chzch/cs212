
"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of 
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**' 
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""
import itertools, re

def write_term(cof,exp):
    if   cof == 0:              return ""
    elif exp == 0:              return str(cof)
    elif cof == 1 and exp == 1: return "x"
    elif cof == 1:              return "x**" + str(exp)
    elif exp == 1:              return str(cof) + " * x"
    else: return str(cof) + " * x**" + str(exp)
    

def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""
    # your code here (I won't repeat "your code here"; there's one for each function)
    terms = []
    for exp, cof in enumerate(coefs):
        terms.append(write_term(cof, exp))
    name = ' + '.join(reversed(filter(lambda t: t is not "", terms)))

    def _f(x):
        f_list = list(name)
        formula = ''.join([str(x) if item == "x" else item for item in f_list]) 
        return eval(formula)
    _f.coefs = coefs
    _f.__name__ = name
    _f.__doc__ = "I am a polynomial."
    return _f


def test_poly():
    global p1, p2, p3, p4, p5, p9 # global to ease debugging in an interactive session

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x**2 + 20 * x + 10
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    assert p9(2) == 512
    p4 =  add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert same_name(power(poly((1, 1)), 10).__name__,
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11,22,33)
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9,18,27) 
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1) 
    assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)

    assert deriv(p1).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573


def same_name(name1, name2):
    """I define this function rather than doing name1 == name2 to allow for some
    variation in naming conventions."""
    def canonical_name(name): return name.replace(' ', '').replace('+-', '-')
    return canonical_name(name1) == canonical_name(name2)


def is_poly(x):
    "Return true if x is a poly (polynomial)."
    ## For examples, see the test_poly function
    return x.__doc__ == "I am a polynomial."


def max_exp(x):
    def _exp(exp):
        if exp[-1] == 'x': 
            e = 1
        else:
            l = len(exp)
            if l == 7: e = exp[-1]
            if l == 5: e = 1
            if l == 4: e = exp[-1]
            if l == 1: e = 0
            if l == 2: e = 1 # there was a bug: f(x) = x + 10
        return e
    return int(max(map(_exp, x)))


def depoly(p):
    terms = p.split(" + ")
    term_list = [re.split(r'[\s\*\*x]', term) for term in terms]
    cofs = [0] * (max_exp(term_list) + 1)
    for sp in term_list:
        length = len(sp)
        if length == 7: cofs[int(sp[-1])] = int(sp[0]) # 5 * x**3
        if length == 5: cofs[1] = int(sp[0]) # 5 * x
        if length == 4: cofs[int(sp[-1])] = 1 # x**3
        if length == 1: cofs[0] = int(sp[0]) # 30
        if length == 2: cofs[1] = 1 # there was a bug: f(x) = x + 10
    return tuple(cofs)


def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."
    return poly(tuple(map(lambda (x, y): x + y, itertools.izip_longest(depoly(p1.__name__), depoly(p2.__name__), fillvalue=0))))


def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    return poly(tuple(map(lambda (x, y): x - y, itertools.izip_longest(depoly(p1.__name__), depoly(p2.__name__), fillvalue=0))))


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."       
    f1 = depoly(p1.__name__)
    f2 = depoly(p2.__name__)
    result = [0] * (len(f1) + len(f2) - 1)
    for exp1, cof1 in enumerate(f1):
        for exp2, cof2 in enumerate(f2):
            result[exp1+exp2] += (cof1*cof2)
    return poly(tuple(result))


def power(p, n):
    "Return a new polynomial which is p to the nth power (n a non-negative integer)."
    def _pow(p, e, n):
        if n == 1: return e
        return _pow(p, mul(p,e),n-1)
    return _pow(p, p, n)  
    


"""
If your calculus is rusty (or non-existant), here is a refresher:
The deriviative of a polynomial term (c * x**n) is (c*n * x**(n-1)).
The derivative of a sum is the sum of the derivatives.
So the derivative of (30 * x**2 + 20 * x + 10) is (60 * x + 20).

The integral is the anti-derivative:
The integral of 60 * x + 20 is  30 * x**2 + 20 * x + C, for any constant C.
Any value of C is an equally good anti-derivative.  We allow C as an argument
to the function integral (withh default C=0).
"""
    
def deriv(p):
    "Return the derivative of a function p (with respect to its argument)."
    d = [exp*cof for exp, cof in enumerate(depoly(p.__name__))][1:]
    return poly(tuple(d))

def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument)."
    i = [cof/(exp+1) for exp, cof in enumerate(depoly(p.__name__))]
    result = [C] + i
    return poly(tuple(result))


"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the 
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,
call the function test_poly1().  Make sure that poly objects can still be called.

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""



def my_test():
    f1 = poly((10,20,30))
    assert f1.__name__ == '30 * x**2 + 20 * x + 10'
    assert is_poly(f1)

    f2 = poly((0,0,0,1))
    assert f2.__name__ == 'x**3'
    assert is_poly(f2)

    f3 = poly((-1,))
    assert f3.__name__  == '-1'
    assert is_poly(f3)

    f4 = poly((30,1))
    assert f4.__name__ == 'x + 30'
    assert is_poly(f3)

    f5 = poly((-10,-20,-1))
    assert f5.__name__ == '-1 * x**2 + -20 * x + -10'

    f6 = poly((0,1))
    assert f6.__name__ == 'x'
    print 'poly tests pass'

    assert depoly(f1.__name__) == (10,20,30) 
    assert depoly(f2.__name__) == (0,0,0,1)
    assert depoly(f3.__name__) == (-1,)
    assert depoly(f4.__name__) == (30,1)
    assert depoly(f5.__name__) == (-10,-20,-1)
    assert depoly(f6.__name__) == (0,1)
    print 'depoly tests pass'

    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')
    print 'is_poly tests pass'
 
    a1 = add(f1,f1)
    assert same_name(a1.__name__, '60 * x**2 + 40 * x + 20')
    a2 = add(f1, f2)
    assert same_name(a2.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')
    a3 = add(f1, f3)
    assert same_name(a3.__name__, '30 * x**2 + 20 * x + 9')
    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11,22,33)
    print 'add tests pass'

    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9,18,27)
    print 'sub tests pass'

    assert deriv(f1).coefs, '(20, 60)'
    assert deriv(a2).coefs, '(20, 60)'
    d1 = deriv(a2)
    assert d1.__name__ == '3 * x**2 + 60 * x + 20'
    assert deriv(f1).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573
    print 'derivatie integral tests pass'

    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    p9 = mul(f2, mul(f2, f2))
    assert p9(2) == 512
  
    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert same_name(power(poly((1, 1)), 10).__name__,
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')
 
    m = poly((1,1)) 
    m2 = mul(m,m)
    print m2.__name__

    m3 = mul(m2,m)
    print m3.__name__

    pw1 = power(m,2)
    print pw1.__name__
    pw2 = power(m,3)
    print pw2.__name__

#my_test()

test_poly()


def test_poly1():
    # I define x as the polynomial 1*x + 0.
    x = poly((0, 1))
    # From here on I can create polynomials by + and * operations on x.
    newp1 =  30 * x**2 + 20 * x + 10 # This is a poly object, not a number!
    assert p1(100) == newp1(100) # The new poly objects are still callable.
    assert same_name(p1.__name__,newp1.__name__)
    assert (x + 1) * (x - 1) == x**2 - 1 == poly((-1, 0, 1))

def test_poly2():
    newp1 = Poly('30 * x**2 + 20 * x + 10')
    assert p1(100) == newp1(100)
    assert same_name(p1.__name__,newp1.__name__)
