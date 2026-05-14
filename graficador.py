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

    # Expresion simbolica -> funcion numpy
    x_func = sp.lambdify(t, xt, modules=['numpy'])

    # Valores de tiempo
    t_vals = np.linspace(t_inicio, t_final, pasos)

    # Evaluacion numerica
    x_vals = np.real(x_func(t_vals))

    # Figura
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#0f1117")
    ax.set_facecolor("#1a1d27")

    ax.plot(t_vals, x_vals, linewidth=1.8, color="#5b8dee")
    ax.set_title(titulo, fontsize=11, color="#e2e8f0", pad=12)
    ax.set_xlabel("Tiempo  t  (s)", color="#94a3b8")
    ax.set_ylabel("Posicion  x(t)", color="#94a3b8")
    ax.axhline(0, linestyle='--', linewidth=0.7, color="#475569")
    ax.tick_params(colors="#94a3b8")
    for spine in ax.spines.values():
        spine.set_edgecolor("#2d3250")
    ax.grid(True, alpha=0.25, color="#334155")
    fig.tight_layout()

    # Retorna la figura. NO llama plt.show()
    # El hilo principal (app.py) se encarga de mostrarla
    return fig