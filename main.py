from resolver_laplace import resolver_laplace


def main():
    #unificar los modulos en el main
    m = 1
    c = 0
    k = 4
    x0 = 1
    xp0 = 0

    Xt = resolver_laplace(m, c, k, x0, xp0)
    print("x(t) =", Xt)

if __name__ == "__main__":
    main ()