import sympy as sp

def resolver_laplace(m, c, k, x0, xp0):
    # definimos las variables independietes si no declaramos real = true sympy trabaja con complejos
    t, s = sp.symbols('t s', real = True)

    numerador = m*(s*x0 + xp0) + c*x0
    denominador = m*s**2 + c*s + k

    #dejamos todo en funcion de s
    Xs = numerador / denominador

    #transformada inversa de laplace
    Xt = sp.inverse_laplace_transform(Xs, s, t)
    Xt = Xt.subs(sp.Heaviside(t), 1)
    return Xt