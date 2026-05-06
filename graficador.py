from sympy import *
import sympy as sp

def graficar_solucion(xt):
    t = sp.symbols('t', real = True)

    sp.plot(xt, (t, 0, 10), title='Solución de la ecuación diferencial', xlabel='Tiempo (t)', ylabel='x(t)')