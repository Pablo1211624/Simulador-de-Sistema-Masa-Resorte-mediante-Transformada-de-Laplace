import sympy as sp

def resolver_laplace(
        m, c, k,
        x0, xp0,
        step_time,
        initial_value,
        final_value):
    
    t, s = sp.symbols('t s', real=True)
    u = sp.Heaviside(t - step_time)
    f_t = initial_value + (final_value - initial_value) * u

    #Transformada de Laplace del STEP
    F_s = sp.laplace_transform(f_t, t, s, noconds=True)

    numerador = F_s + m*(s*x0 + xp0) + c*x0
    denominador = m*s**2 + c*s + k

    Xs = numerador / denominador

    #Inversa de Laplace
    Xt = sp.inverse_laplace_transform(Xs, s, t)

    Xt = sp.simplify(Xt)

    Xt = Xt.subs(sp.Heaviside(t), 1)
    return Xt
