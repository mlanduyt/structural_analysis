import numpy as np
import sympy as sym
tol = 0.01

def newtons_method(f, x0: float, tol: float = 1e-6, max_iter: int = 100, h: float = 1e-5) -> float:

    x = x0
    for i in range(max_iter):
        fx = f(x)
        dfx = (f(x + h) - f(x)) / h  

        if abs(dfx) < 1e-8:
            raise ValueError("Derivative near zero.")

        x_n = x - fx / dfx

        if abs(x_n - x) < tol:
            return x_n

        x = x_n
    raise ValueError("Maximum number of iterations exceeded.")