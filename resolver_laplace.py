import sympy as sp

def resolver_laplace(
        m, c, k,
        x0, xp0):
    
    s, t = sp.symbols("s t", real=True, positive=True)

    m  = sp.Rational(str(m))
    b  = sp.Rational(str(c))
    k  = sp.Rational(str(k))
    x0 = sp.Rational(str(x0))
    v0 = sp.Rational(str(xp0))

    X_s = (m*s*x0 + m*v0 + b*x0) / (m*s**2 + b*s + k)

    x_t = sp.inverse_laplace_transform(X_s, s, t)
    x_t = sp.simplify(x_t)
    x_t = sp.nsimplify(x_t)

    return x_t
