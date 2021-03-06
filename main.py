import operator as op
import random as rand
import math as m
import numpy as np
import matplotlib.pyplot as mpl


def toint(Num):
    if Num[0] == 'b':
        Num = int(Num[1:], 2)
    elif len(Num) > 1 and Num[1] == 'x':
        Num = int(Num[2:], 16)
    else:
        Num = int(Num)
    return Num


def collect_data():
    g = input('Insert g(x).(prefix "b" for binary input, "0x" for hex, no prefix for decimal.) ')
    g = toint(g)
    l = int(input('Insert message length. (decimal) '))
    d = int(input('Insert code distance. (decimal) '))
    #epsilon = float(input('Insert accuracy of the decoding error probability(epsilon). '))
    #p = float(input('Insert p. '))
    return g, l, d


def checksum(a, g, n, r):
    i = 1
    while (a >> r-1) > 1:
        if a >> n - i == 1:
            a = op.xor(a, g << (n - r - i))
            i += 1
        else:
            i += 1
    return a


def errVector(p, n):
    n -= 1
    errV = 0
    while n >= 0:
        bit = rand.random()
        if bit <= p:
           bit = 1
        else:
           bit = 0
        bit = bit << n
        errV = errV + bit
        n -= 1
    return errV


def upperDecoding(d, p, n):
    sum = 0
    i = 0
    while i < d:
        sum = sum + (m.factorial(n)/(m.factorial(i)*m.factorial(n-i))) * p**i * (1-p)**(n-i)
        i += 1
    return (1 - sum)


def weight(num, length):
    i = 1
    w = 0
    while i <= length:
        tmp = num >> (length - i)
        if ((num >> (length - i)) & 1) == 1:
            w += 1
        i += 1
    return w


def GenPePuPLists(d, n, A):
    c = 0
    Pu = []
    Pe = []
    P = []
    for p in np.arange(0, 1, 0.01):
        P.insert(c, p)
        Pu.insert(c, upperDecoding(d, p, n))
        i = d
        pe = 0
        while i <= n:
            pe = pe + A[i] * p ** i * (1 - p) ** (n - i)
            i += 1
        Pe.insert(c, pe)
        c += 1
    return Pe, Pu, P


def graphics(P, Pe, Pu, mark):
    mpl.plot(P, Pe, (mark + 'r'))
    mpl.xlabel('p')
    mpl.ylabel('Pe(red), Pu(green)')
    mpl.plot(P, Pu, (mark + 'g'))
    return 1


def main(g, l, d):
    r = -1
    tmp = g
    while tmp != 0:
        tmp = tmp >> 1
        r += 1
    n = l + r
    m = 1
    A = {a: 0 for a in range(n+1)}
    while m < 2**l:
        a = m << r
        c = checksum(a, g, n, r)
        a = a + c
        w = weight(a, n)
        A[w] += 1
        m += 1
    return n, A

    '''N = 9/(4*epsilon**2)
    Ne = 0
    while N > 0:
        e = errVector(p, n)
        b = op.xor(a, e)
        syndrome = checksum(b, g, n, r)
        if e != 0 and syndrome == 0:
            Ne += 1
        N -= 1
    N = 9 / (4 * epsilon ** 2)
    PeImitated = Ne / N'''


if __name__ == '__main__':
    g, l, d = collect_data()

    nL, AL = main(g, (l - 1), d)
    PeL, PuL, PL = GenPePuPLists(d, nL, AL)
    graphics(PL, PeL, PuL, '--')

    n, A = main(g, l, d)
    Pe, Pu, P = GenPePuPLists(d, n, A)
    graphics(P, Pe, Pu, '-.')

    nG, AG = main(g, (l + 1), d)
    PeG, PuG, PG = GenPePuPLists(d, nG, AG)
    graphics(PG, PeG, PuG, '+')

    mpl.show()
