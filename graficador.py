import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def graficar_solucion(
        xt,
        t_inicio=0,
        t_final=10,
        pasos=500,
        titulo="Sistema Masa-Resorte"):

    t = sp.symbols('t', real=True)

    #Convertimos expresion simbolica a funcion numpy
    x_func = sp.lambdify(t, xt, modules=['numpy'])

    #Valores de tiempo
    t_vals = np.linspace(t_inicio, t_final, pasos)

    #Evaluacion numerica
    x_vals = np.real(x_func(t_vals))

    #Garfica
    plt.figure(figsize=(10, 5))

    plt.plot(
        t_vals,
        x_vals,
        linewidth=1.8
    )

    plt.title(titulo, fontsize=13)

    plt.xlabel("Tiempo t (s)")
    plt.ylabel("Posicion x(t)")

    plt.axhline(
        0,
        linestyle='--',
        linewidth=0.7
    )

    plt.grid(True, alpha=0.4)
    plt.tight_layout()
    plt.show(block=True)
    
