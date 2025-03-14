import numpy as np
from bisection import *
import os
from pathlib import Path

def test_error ():
    f = lambda x: 2*(x+2)
    tol = 0.01
    a = -5
    b = 10
    # Call the bisection method
    root = bisection (f, a, b, tol)

    #Define Error, expected answer = -2
    error = root + 2
    assert tol>error

def test_falsereturn ():
    f = lambda x: (x)
    tol = 0.01
    a = 10
    b = 5
    # Call the bisection method
    root = bisection (f, a, b, tol)
    #Define Error, expected answer = 0
    error = root 
    assert tol>error

def test_input():
    f = lambda x: x
    tol = 0.01
    z = a+b
    assert z < 100.1

def test_tol():
    assert tol == 0.01

def test_list():
    if a > 50:
        assert False
    elif a < -50:
        assert False
    else:
        assert True

def test_zero ():
    f = lambda x: x
    a = -5
    b = 5
    # Call the bisection method
    root = bisection (f, a, b, tol)

    #Define Error, expected answer = 0
    error = root 
    assert tol>error

def test_midpoint ():
    a = 0
    b = 2
    m = (1/2)*(a+b)
    assert m == 1

def test_sign ():
    f = lambda x: x*2
    a = 2
    sign = np.sign(f(a))
    assert sign > 0

def test_abs ():
    f = lambda x: x*2
    a = -2
    b = np.abs(f(a))
    assert b > 0

def test_opp ():
    f = lambda x: x*2
    a = 2
    b = -2
    assert np.sign(f(a)) != np.sign(f(b))

def test_quadratic ():
    f = lambda x: (x**2)
    tol = 0.1
    a = 1
    b = -1
    # Call the bisection method
    root = bisection (f, a, b, tol)

    #Define Error, expected answer = 0
    error = root*0.1
    assert tol>error

def test_random ():
    a = random.choice(list1)
    if a > 50:
        assert False
    elif a < -50:
        assert False
    else:
        assert True

def test_sum ():
    a = 2
    b = 3
    assert a+b ==5

def test_multi ():
    a = 2
    b = 3
    assert a*b == 6

def test_div ():
    a = 2
    b = 1
    assert a/b == 2

def test_sub ():
    a = 2
    b = 1
    assert a-b == 1

def test_negative ():
    a = -1
    b = 1
    assert a*b < 0

def test_print ():
    a = 1
    print (a)
    assert a == 1

def test_elif ():
    a = random.choice(list1)
    b = random.choice(list1)
    if a > b:
        assert True
    elif b > a :
        assert True
    else: 
        assert True

def test_i ():
    for i in range (2):
        k = i+1
        assert k > 0

