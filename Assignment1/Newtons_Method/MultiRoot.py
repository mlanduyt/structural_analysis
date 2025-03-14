#Import Info from other scripts
import numpy as np
import random
from function import *
import os
from pathlib import Path
from sympy import symbols, diff, lambdify
x = symbols('x')

#Define Example function
f = [2*x, 2*x+3]
list1 = range (-50,50)
tol = 0.001

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

def multi_function (eqns): 
    for i in range (0,2):
        f = eqns[i]
        root == multi_root(eqns)
        print (root)
        return root
        

x0 = 3
x = sym.symbols('x')
eqns = ((x*2)-1, x)
n = 2
roots = multi_function(eqns)
print (roots)