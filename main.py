import tkinter as tk
from tkinter import ttk, messagebox
import threading
import math
import sympy as sp

from resolver_laplace import resolver_laplace
from graficador import graficar_solucion

EJERCICIOS = [
    {
        "nombre": "Ejercicio 1",
        "m": 10,    
        "b": 0.4,  
        "k": 0.16,
        "x0": 0.25,    
        "v0": 0,
        "t_inicio": 0,  
        "t_final": 300, 
        "pasos": 600
    },
    {
        "nombre": "Ejercicio 2",
        "m": 4,     
        "b": 0,    
        "k": 16,
        "x0": 0.25,    
        "v0": 0,
        "t_inicio": 0,  
        "t_final": 10,  
        "pasos": 500
    },
    {
        "nombre": "Ejercicio 3",
        "m": 10,    
        "b": 0.2,  
        "k": 0.04,
        "x0": 0.25,    
        "v0": 0,
        "t_inicio": 0,  
        "t_final": 300, 
        "pasos": 600
    },
    {
        "nombre": "Ejercicio 4",
        "m": 150,   
        "b": 4.5,  
        "k": 0.03,
        "x0": 0.25,    
        "v0": 0,
        "t_inicio": 0,  
        "t_final": 1000,
        "pasos": 800
    },
    {
        "nombre": "Ejercicio 5",
        "m": 50,    
        "b": 2,    
        "k": 0.02,
        "x0": 0.25,    
        "v0": 0,
        "t_inicio": 0,  
        "t_final": 1000,
        "pasos": 800
    },
]

BG        = "#0f1117"
BG2       = "#1a1d27"
BG3       = "#22263a"
ACCENT    = "#5b8dee"
ACCENT2   = "#a78bfa"
GREEN     = "#34d399"
ORANGE    = "#fb923c"
TEXT      = "#e2e8f0"
MUTED     = "#64748b"
BORDER    = "#2d3250"

FONT_TITLE  = ("Consolas", 18, "bold")
FONT_SECTION= ("Consolas", 10, "bold")
FONT_LABEL  = ("Consolas", 9)
FONT_ENTRY  = ("Consolas", 10)
FONT_BTN    = ("Consolas", 10, "bold")
FONT_RESULT = ("Consolas", 9)

def formatear_solucion(expr):
    expr = sp.simplify(expr)
    expr = sp.nsimplify(expr)

    texto = sp.pretty(expr, use_unicode=True)

    return f"x(t) =\n{texto}"


def clasificar_amortiguamiento(m, b, k):
    discriminante = b**2 - 4 * m * k
    omega_n = math.sqrt(k / m)
    zeta    = b / (2 * math.sqrt(m * k)) if b > 0 else 0

    if b == 0:
        tipo = "SIN Amortiguamiento"
    elif abs(discriminante) < 1e-9:
        tipo = "Amortiguamiento Critico"
    elif discriminante > 0:
        tipo = "SOBRE Amortiguado"
    else:
        tipo = "SUB Amortiguado"

    return tipo, discriminante, omega_n, zeta


def make_label(parent, text, row, col, color=TEXT, font=FONT_LABEL,
               sticky="w", padx=8, pady=3, columnspan=1):
    tk.Label(parent, text=text, bg=BG2, fg=color, font=font)\
      .grid(row=row, column=col, columnspan=columnspan,
            sticky=sticky, padx=padx, pady=pady)

def make_entry(parent, row, col, width=14, default=""):
    frame = tk.Frame(parent, bg=ACCENT, padx=1, pady=1)
    frame.grid(row=row, column=col, padx=8, pady=3, sticky="w")
    e = tk.Entry(frame, width=width, bg=BG3, fg=TEXT,
                 insertbackground=ACCENT, relief="flat",
                 font=FONT_ENTRY, bd=4)
    e.pack()
    if default != "":
        e.insert(0, str(default))
    return e

def make_section(parent, text, row, col, columnspan=1, padx=10, pady=(10,4)):
    lf = tk.LabelFrame(
        parent, text=f"  {text}  ",
        bg=BG2, fg=ACCENT, font=FONT_SECTION,
        bd=1, relief="flat",
        highlightbackground=BORDER, highlightthickness=1
    )
    lf.grid(row=row, column=col, columnspan=columnspan,
            padx=padx, pady=pady, sticky="nsew")
    return lf

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Masa-Resorte  ·  Laplace")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG, pady=10)
        header.grid(row=0, column=0, sticky="ew")

        tk.Label(header, text="SIMULADOR  MASA-RESORTE",
                 bg=BG, fg=ACCENT, font=FONT_TITLE).pack()
        tk.Label(header,
                 text="mx''(t) + bx'(t) + kx(t) = 0   —   Transformada de Laplace",
                 bg=BG, fg=MUTED, font=("Consolas", 9)).pack()


        tk.Frame(self.root, bg=ACCENT, height=2)\
          .grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 8))


        body = tk.Frame(self.root, bg=BG)
        body.grid(row=2, column=0, padx=10, pady=4)

        self._build_presets(body)
        self._build_params(body)
        self._build_footer()
        self.cargar_ejercicio(0)

    def _build_presets(self, parent):
        sec = make_section(parent, "Ejercicios precargados", 0, 0, columnspan=3, pady=(0, 6))

        colors = [
            ("#1e40af", "#93c5fd"),
            ("#5b21b6", "#c4b5fd"),
            ("#065f46", "#6ee7b7"),
            ("#7c2d12", "#fdba74"),
            ("#164e63", "#67e8f9"),
        ]
        for i, ej in enumerate(EJERCICIOS):
            bg_btn, fg_btn = colors[i]
            btn = tk.Button(
                sec,
                text=ej["nombre"],
                bg=bg_btn, fg=fg_btn,
                font=FONT_BTN,
                relief="flat", cursor="hand2",
                activebackground=fg_btn, activeforeground=bg_btn,
                width=13, pady=6,
                command=lambda idx=i: self.cargar_ejercicio(idx)
            )
            btn.grid(row=0, column=i, padx=8, pady=8)


        tk.Button(
            sec,
            text="+ Manual",
            bg=BG3, fg=ACCENT2,
            font=FONT_BTN,
            relief="flat", cursor="hand2",
            activebackground=ACCENT2, activeforeground=BG,
            width=13, pady=6,
            command=self.limpiar_campos
        ).grid(row=0, column=5, padx=8, pady=8)


    def _build_params(self, parent):
        #Columna 0
        sys_f = make_section(parent, "Parametros del sistema", 1, 0)
        sys_f.configure(bg=BG2)

        labels_sys = [
            ("Masa  m  (kg)",        "e_m"),
            ("Amortiguamiento  b",   "e_b"),
            ("Constante resorte  k", "e_k"),
            ("Posicion inicial x(0)","e_x0"),
            ("Velocidad inicial x'(0)","e_v0"),
        ]
        for i, (lbl, attr) in enumerate(labels_sys):
            make_label(sys_f, lbl, i, 0)
            entry = make_entry(sys_f, i, 1)
            setattr(self, attr, entry)

        #COlumna 1
        sim_f = make_section(parent, "Configuracion de simulacion", 1, 1, padx=6)

        labels_sim = [
            ("Tiempo inicial",   "e_t0"),
            ("Tiempo final",     "e_tf"),
            ("Numero de Pasos",   "e_pasos"),
        ]
        for i, (lbl, attr) in enumerate(labels_sim):
            make_label(sim_f, lbl, i, 0)
            entry = make_entry(sim_f, i, 1)
            setattr(self, attr, entry)  

        #Columna 2
        res_f = make_section(parent, "Resultados calculados", 1, 2)

        def res_row(text, row, color=GREEN):
            make_label(res_f, text, row, 0, color=MUTED, font=("Consolas", 8))
            var = tk.StringVar(value="—")
            lbl = tk.Label(res_f, textvariable=var,
                           bg=BG2, fg=color,
                           font=("Consolas", 10, "bold"),
                           anchor="w", width=26)
            lbl.grid(row=row + 1, column=0, padx=8, pady=(0, 6), sticky="w")
            return var

        self.var_tipo  = res_row("Tipo de amortiguamiento", 0, ORANGE)
        self.var_wn    = res_row("Frecuencia natural  wn (rad/s)", 2)
        self.var_zeta  = res_row("Factor amortiguamiento", 4)
        self.var_disc  = res_row("Discriminante  b² − 4mk", 6)

        make_label(res_f, "Solucion  x(t) =", 8, 0, color=MUTED, font=("Consolas", 8))
        self.lbl_xt = tk.Label(
            res_f, text="—",
            bg=BG2, fg=ACCENT2,
            font=("Consolas", 8),
            anchor="nw", justify="left",
            width=70, wraplength=260, height=12
        )
        self.lbl_xt.grid(row=9, column=0, padx=8, pady=(0, 6), sticky="w")



    def _build_footer(self):
        foot = tk.Frame(self.root, bg=BG, pady=8)
        foot.grid(row=3, column=0, sticky="ew")

        self.lbl_status = tk.Label(
            foot, text="Listo.",
            bg=BG, fg=MUTED, font=("Consolas", 9)
        )
        self.lbl_status.pack()
        

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Blue.Horizontal.TProgressbar",
                        troughcolor=BG3, background=ACCENT,
                        thickness=4)
        self.progress = ttk.Progressbar(
            foot, mode="indeterminate", length=520,
            style="Blue.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(4, 8))

        self.btn_sim = tk.Button(
            foot,
            text="  :)  SIMULAR  ",
            bg=ACCENT, fg=BG,
            font=("Consolas", 13, "bold"),
            relief="flat", cursor="hand2",
            activebackground=ACCENT2, activeforeground=BG,
            padx=30, pady=10,
            command=self.simular
        )
        self.btn_sim.pack()

    def cargar_ejercicio(self, idx):
        ej = EJERCICIOS[idx]
        pares = [
            (self.e_m,         ej["m"]),
            (self.e_b,         ej["b"]),
            (self.e_k,         ej["k"]),
            (self.e_x0,        ej["x0"]),
            (self.e_v0,        ej["v0"]),
            (self.e_t0,        ej["t_inicio"]),
            (self.e_tf,        ej["t_final"]),
            (self.e_pasos,     ej["pasos"]),
        ]
        for entry, val in pares:
            entry.delete(0, tk.END)
            entry.insert(0, str(val))
        self.lbl_status.config(text=f"Cargado: {ej['nombre']}")

    def limpiar_campos(self):
        for attr in ("e_m","e_b","e_k","e_x0","e_v0",
                     "e_t0","e_tf","e_pasos"):
            getattr(self, attr).delete(0, tk.END)
        self.lbl_status.config(text="Modo manual — ingresa los parametros.")

    def simular(self):
        try:
            m             = float(self.e_m.get())
            b             = float(self.e_b.get())
            k             = float(self.e_k.get())
            x0            = float(self.e_x0.get())
            v0            = float(self.e_v0.get())
            t_inicio      = float(self.e_t0.get())
            t_final       = float(self.e_tf.get())
            pasos         = int(self.e_pasos.get())

        except ValueError:
            messagebox.showerror("Error de entrada",
                                 "Revisa los valores ingresados.\nTodos deben ser numeros.")
            return

        if m <= 0 or k <= 0:
            messagebox.showerror("Error", "m y k deben ser > 0")
            return
        if b < 0:
            messagebox.showerror("Error", "b debe ser >= 0")
            return
        if t_final <= t_inicio:
            messagebox.showerror("Error", "Tiempo final debe ser mayor al tiempo inicial")
            return
        if pasos < 50:
            messagebox.showerror("Error", "Numero de pasos debe ser >= 50")
            return

        tipo, disc, omega_n, zeta = clasificar_amortiguamiento(m, b, k)
        self.var_tipo.set(tipo)
        self.var_wn.set(f"{omega_n:.6f} rad/s")
        self.var_zeta.set(f"{zeta:.6f}")
        self.var_disc.set(f"{disc:.6f}")
        self.lbl_xt.config(text="Calculando...")
        self.lbl_status.config(text="Resolviendo ecuacion diferencial por Laplace")
        self.btn_sim.config(state="disabled")
        self.progress.start(10)

        titulo = f"{tipo}  |  wn={omega_n:.3f}  |  zeta={zeta:.3f}"

        def run():
            try:
                Xt = resolver_laplace(m, b, k, x0, v0)

                self.root.after(0, lambda: _mostrar(Xt))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error en simulacion", str(e)))
                self.root.after(0, lambda: self.lbl_status.config(text="Error en la simulacion."))
            finally:
                self.root.after(0, self.progress.stop)
                self.root.after(0, lambda: self.btn_sim.config(state="normal"))

        def _mostrar(Xt):
            import matplotlib.pyplot as plt
            self.lbl_xt.config(text=formatear_solucion(Xt))
            self.lbl_status.config(text="Generando grafica...")
            try:
                graficar_solucion(
                    Xt,
                    t_inicio=t_inicio,
                    t_final=t_final,
                    pasos=pasos,
                    titulo=titulo
                )
                plt.show(block=False)
                self.lbl_status.config(text="Listo.")
            except Exception as e:
                messagebox.showerror("Error al graficar", str(e))
                self.lbl_status.config(text="Error al graficar.")

        threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()