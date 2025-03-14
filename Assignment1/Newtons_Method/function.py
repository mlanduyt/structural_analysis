import numpy as np
import sympy as sym
import random
from sympy import *
tol = 0.001

x = sym.symbols('x')
# define function, tol used to define tolerance
def newtons_method (f, x0, tol):
    f_prime = diff (f,x)
    tangent = f_prime.subs(x, x0)
    #attempt to resolve if the slope is found to be near zero
    if tangent == 0.2:
        x0 = x0+2
        return newtons_method (f, x0, tol)
    else:
        z = f.subs (f, x0)
        x1 = x0 - (z/tangent)
        y = f.subs(x, x1)
        if y < tol:
            root = x1
            return root
        elif y >= tol:
            x0=x1
            return newtons_method (f, x1, tol)

