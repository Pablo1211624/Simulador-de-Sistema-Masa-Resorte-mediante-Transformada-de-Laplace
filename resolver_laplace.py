import sympy as sp

def resolver_laplace(m, c, k, x0, xp0):
    # definimos las variables independietes
    t, s = sp.symbols('t s')

    numerador = m(s*x0 + xp0) + c*x0
    denominador = m*s**2 + c*s + k

    #dejamos todo en funcion de s
    Xs = numerador / denominador

    #transformada inversa de laplace
    Xt = sp.inverse_laplace_transform(Xs, s, t)

    return Xt