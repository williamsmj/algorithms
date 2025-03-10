'''
Implement basic arithmetic operations using the following bit-based primitives:

 - test x for even
 - double x
 - floor divide x by 2, i.e. halve

and integer addition/subtraction, comparison of two integers, and test for
equality to zero.
'''
import random


def even(x):
    return False if x & 1 else True


def double(x):
    return x << 1


def halve(x):
    return x >> 1


def multpos(x, y):
    '''Multiply two positive integers using the French method.'''
    if y == 0:
        return 0
    z = multpos(x, halve(y))
    if even(y):
        return double(z)
    else:
        return x + double(z)


def mult(x, y):
    '''Multiply two integers.'''
    if x < 0 and y >= 0:
        return -multpos(-x, y)
    elif x >= 0 and y < 0:
        return -multpos(x, -y)
    elif x < 0 and y < 0:
        return multpos(-x, -y)
    else:
        return multpos(x, y)


def square(x):
    return mult(x, x)


def divnonneg(x, y):
    '''
    Divide two non-negative integers, returning quotient and remainder.

    On division of x by zero quotient = 0 and remainder = x.
    '''

    if x < 0 or y < 0:
        raise ValueError
    if x == 0:
        return 0, 0
    if y == 0:
        return 0, x
    q, r = divnonneg(halve(x), y)
    q = double(q)
    r = double(r)
    if not even(x):
        r += 1
    if r >= y:
        r -= y
        q += 1
    return q, r


def div(x, y):
    if x == 0:
        return 0, 0
    if y == 0:
        return 0, x

    q, r = divnonneg(max(-x, x), max(y, -y))
    if x > 0 and y > 0:
        return q, r
    if x < 0 and y > 0:
        return (-q, 0) if r == 0 else (-q - 1, y - r)
    if x > 0 and y < 0:
        return (-q, 0) if r == 0 else (-q - 1, y + r)
    if x < 0 and y < 0:
        return q, -r


def mod(x, N):
    '''Return x mod N.'''
    return div(x, N)[1]


def modexp(x, y, N=0):
    '''Return x^y mod N.'''
    if y < 0:
        raise ValueError('y must be non-negative.')
    if max(N, -N) == 1:  # any number mod 1 or mod -1 is 1
        return 0
    if y == 0:
        return mod(1, N)
    z = modexp(x, halve(y), N)
    if even(y):
        return mod(square(z), N)
    else:
        return mod(mult(x, square(z)), N)


def gcd(a, b):
    '''
    Return gcd(a, b) using Euclid's algorithm.
    '''
    if b == 0:
        return max(a, -a)
    else:
        return gcd(b, mod(a, b))


def quotient(x, N):
    '''Return x//N'''
    return div(x, N)[0]


def egcd(a, b):
    '''Returns x, y, d such that d = gcd(a, b) and ax + by = d.'''
    if b == 0:
        if a < 0:
            return -1, 0, -a
        else:
            return 1, 0, a
    xprime, yprime, dprime = egcd(b, mod(a, b))
    x = yprime
    y = xprime - mult(quotient(a, b), yprime)
    d = dprime
    return x, y, d


def multinv(a, N):
    '''
    Returns the multiplicative inverse of a modulo N, i.e. x such that ax ≡ 1
    (mod N). This does not exist if the greatest common divisor of a and N ≠ 1,
    i.e. if a and N are not relatively prime.
    '''
    if a == 0:
        raise ValueError('a must be non-zero.')
    if N <= 1:
        raise ValueError('N must greater than 1.')

    x, y, d = egcd(a, N)
    if d != 1:
        raise ValueError('a and N are not relatively prime.')
    else:
        return mod(x, N)


def prime(N, k=100, a=None):
    '''
    Returns True if a number is probably prime, False if it is definitely not.

    By definition negative numbers are not prime.

    If a is None this uses k applications of Fermat's Little Theorem.
    Probability of failure (i.e. probability returns True if not a prime) is
    < 1/2^k.

    If a is an iterable, it performs the test for those values of a.
    '''
    if N <= 0:
        return False

    def fermat_test(a):
        return modexp(a, N-1, N) == 1

    if a is None:
        if k >= N:
            k = N - 1
        a = random.sample(range(1, N), k)
    else:
        a = [ai for ai in a if ai < N]

    return all(fermat_test(ai) for ai in a)


def randomprime(n):
    '''
    Returns a random prime that is no more than n bits long.
    '''
    Nmax = modexp(2, n) - 1
    while True:
        N = random.randint(2, Nmax)
        if prime(N, a=(2, 3, 5)):
            return N


def lcm(a, b):
    '''Return the lowest common multiple of integers a and b.'''
    return quotient(mult(a, b), gcd(a, b))
