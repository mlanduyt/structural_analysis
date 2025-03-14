#Import Info from other scripts
import numpy as np
import random
from Newtons import *
import os
from pathlib import Path
from sympy import symbols, diff, lambdify
x = symbols('x')

n = 2
#Used to evaluate method 4 times, outputs second root if found
def multi_root(f):
    for i in range (1,n):
        x0 = random.choice (list1)
        root1 = newtons_method (f, x0, tol)
        x3 = random.choice (list1)
        root2 = newtons_method (f, x3, tol)
        if root2-root1 < 2*tol:
            x0 = x0*-1
            root3 = newtons_method(f,x0, tol)
            if root3-root1 < 2*tol:
                x0 = random.choice (list1)
                root4 = newtons_method(f,x0,tol)
                if root4-root1 < 2*tol:
                    #print (root1)
                    roots = [root1]
                    return roots
                else:
                    #print (root4) and (root1)
                    roots = [root1, root4]
                    return roots
            else:
                #print (root3) and (root1)
                roots = [root1, root3]
                return roots
        else:
            #print (root1) and (root2)
            roots = [root1, root2]
            return roots

def multi_function (eqns, x0, n):
    for i in range (n):
        f = eqns[i]
        root = newtons_method (f, x0)
        print ('root=', root)