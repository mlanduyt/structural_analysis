import numpy as np
from Newtons import *
from MultiRoot import *
import os
from pathlib import Path

def test_error ():
    f = lambda x: 2*(x+2)
    tol = 0.01
    x0 = 0
    root = newtons_method (f, x0, tol)
    #Define Error, expected answer = -2
    error = root + 2
    if tol > error:
        print ("test passed")
    else:
        print ("test failed")

def test_quadratic():
    f = lambda x: x**2 - 4
    root1 = newtons_method(f, 1.0, tol=1e-6)
    assert abs(root1 - 2) < 1e-6, "Quadratic test failed"

def test_no_real_root():
    f = lambda x: x**2 + 1
    try:
        newtons_method(f, 1.0)
        assert False, "No real root test failed (Expected ValueError)"
    except ValueError as e:
        assert "Maximum number of iterations exceeded" in str(e), "Unexpected error message"

def test_near_zero():
    f = lambda x: x**3
    try:
        newtons_method(f, 0.0)
        assert False, "Derivative too close to zero (Expected ValueError)"
    except ValueError as e:
        assert "Derivative too close to zero"
    

    
    



