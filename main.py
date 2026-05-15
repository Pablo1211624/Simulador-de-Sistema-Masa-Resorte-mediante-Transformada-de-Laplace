import tkinter as tk
from tkinter import ttk, messagebox
import threading
import math
import sympy as sp
import numpy as np

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

FONT_TITLE   = ("Consolas", 18, "bold")
FONT_SECTION = ("Consolas", 10, "bold")
FONT_LABEL   = ("Consolas", 9)
FONT_ENTRY   = ("Consolas", 10)
FONT_BTN     = ("Consolas", 10, "bold")


def formatear_solucion(expr):
    expr = sp.simplify(expr)
    expr = sp.nsimplify(expr)
    texto = sp.pretty(expr, use_unicode=True)
    return "x(t) =\n\n" + texto


def clasificar_amortiguamiento(m, b, k):
    discriminante = b**2 - 4 * m * k
    omega_n = math.sqrt(k / m)
    zeta = b / (2 * math.sqrt(m * k)) if b > 0 else 0

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

    e = tk.Entry(
        frame,
        width=width,
        bg=BG3,
        fg=TEXT,
        insertbackground=ACCENT,
        relief="flat",
        font=FONT_ENTRY,
        bd=4
    )
    e.pack()

    if default != "":
        e.insert(0, str(default))

    return e


def make_section(parent, text, row, col, columnspan=1, padx=10, pady=(10, 4)):
    lf = tk.LabelFrame(
        parent,
        text=f"  {text}  ",
        bg=BG2,
        fg=ACCENT,
        font=FONT_SECTION,
        bd=1,
        relief="flat",
        highlightbackground=BORDER,
        highlightthickness=1
    )
    lf.grid(
        row=row,
        column=col,
        columnspan=columnspan,
        padx=padx,
        pady=pady,
        sticky="nsew"
    )
    return lf


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador Masa-Resorte  ·  Laplace")
        self.root.geometry("1030x720")
        self.root.minsize(900, 600)
        self.root.resizable(True, True)
        self.root.configure(bg=BG)

        try:
            self.root.state("zoomed")
        except:
            pass

        self.animando = False
        self.anim_index = 0
        self.anim_t_vals = []
        self.anim_x_vals = []

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg=BG, pady=10)
        header.grid(row=0, column=0, sticky="ew")

        tk.Label(
            header,
            text="SIMULADOR  MASA-RESORTE",
            bg=BG,
            fg=ACCENT,
            font=FONT_TITLE
        ).pack()

        tk.Label(
            header,
            text="mx''(t) + bx'(t) + kx(t) = 0   —   Transformada de Laplace",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 9)
        ).pack()

        tk.Frame(self.root, bg=ACCENT, height=2)\
            .grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 8))

        contenedor = tk.Frame(self.root, bg=BG)
        contenedor.grid(row=2, column=0, sticky="nsew")

        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.scroll_canvas = tk.Canvas(
            contenedor,
            bg=BG,
            highlightthickness=0
        )
        self.scroll_canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(
            contenedor,
            orient="vertical",
            command=self.scroll_canvas.yview
        )
        scrollbar.pack(side="right", fill="y")

        self.scroll_canvas.configure(yscrollcommand=scrollbar.set)

        self.body = tk.Frame(self.scroll_canvas, bg=BG)

        self.scroll_canvas.create_window(
            (0, 0),
            window=self.body,
            anchor="nw"
        )

        self.body.bind(
            "<Configure>",
            lambda e: self.scroll_canvas.configure(
                scrollregion=self.scroll_canvas.bbox("all")
            )
        )

        self.root.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind_all("<Button-4>", lambda e: self.scroll_canvas.yview_scroll(-1, "units"))
        self.root.bind_all("<Button-5>", lambda e: self.scroll_canvas.yview_scroll(1, "units"))

        self._build_presets(self.body)
        self._build_params(self.body)
        self._build_animacion(self.body)
        self._build_footer(self.body)

        self.cargar_ejercicio(0)

    def _on_mousewheel(self, event):
        self.scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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
                bg=bg_btn,
                fg=fg_btn,
                font=FONT_BTN,
                relief="flat",
                cursor="hand2",
                activebackground=fg_btn,
                activeforeground=bg_btn,
                width=12,
                pady=6,
                command=lambda idx=i: self.cargar_ejercicio(idx)
            )
            btn.grid(row=0, column=i, padx=5, pady=8)

        tk.Button(
            sec,
            text="+ Manual",
            bg=BG3,
            fg=ACCENT2,
            font=FONT_BTN,
            relief="flat",
            cursor="hand2",
            activebackground=ACCENT2,
            activeforeground=BG,
            width=12,
            pady=6,
            command=self.limpiar_campos
        ).grid(row=0, column=5, padx=5, pady=8)

        self.btn_sim = tk.Button(
            sec,
            text="SIMULAR",
            bg=ACCENT,
            fg=BG,
            font=("Consolas", 11, "bold"),
            relief="flat",
            cursor="hand2",
            activebackground=ACCENT2,
            activeforeground=BG,
            width=12,
            pady=6,
            command=self.simular
        )
        self.btn_sim.grid(row=0, column=6, padx=5, pady=8)

    def _build_params(self, parent):
        sys_f = make_section(parent, "Parametros del sistema", 1, 0)
        sys_f.configure(bg=BG2)

        labels_sys = [
            ("Masa  m  (kg)", "e_m"),
            ("Amortiguamiento  b", "e_b"),
            ("Constante resorte  k", "e_k"),
            ("Posicion inicial x(0)", "e_x0"),
            ("Velocidad inicial x'(0)", "e_v0"),
        ]

        for i, (lbl, attr) in enumerate(labels_sys):
            make_label(sys_f, lbl, i, 0)
            entry = make_entry(sys_f, i, 1)
            setattr(self, attr, entry)

        sim_f = make_section(parent, "Configuracion de simulacion", 1, 1, padx=6)

        labels_sim = [
            ("Tiempo inicial", "e_t0"),
            ("Tiempo final", "e_tf"),
            ("Numero de Pasos", "e_pasos"),
        ]

        for i, (lbl, attr) in enumerate(labels_sim):
            make_label(sim_f, lbl, i, 0)
            entry = make_entry(sim_f, i, 1)
            setattr(self, attr, entry)

        res_f = make_section(parent, "Resultados calculados", 1, 2)

        def res_row(text, row, color=GREEN):
            make_label(res_f, text, row, 0, color=MUTED, font=("Consolas", 8))

            var = tk.StringVar(value="—")

            lbl = tk.Label(
                res_f,
                textvariable=var,
                bg=BG2,
                fg=color,
                font=("Consolas", 10, "bold"),
                anchor="w",
                width=26
            )
            lbl.grid(row=row + 1, column=0, padx=8, pady=(0, 6), sticky="w")

            return var

        self.var_tipo = res_row("Tipo de amortiguamiento", 0, ORANGE)
        self.var_wn = res_row("Frecuencia natural  wn (rad/s)", 2)
        self.var_zeta = res_row("Factor amortiguamiento", 4)
        self.var_disc = res_row("Discriminante  b² − 4mk", 6)

        make_label(res_f, "Solucion  x(t) =", 8, 0, color=MUTED, font=("Consolas", 8))

        self.lbl_xt = tk.Text(
            res_f,
            bg=BG2,
            fg=ACCENT2,
            font=("Consolas", 9),
            width=52,
            height=14,
            wrap="none",
            relief="flat",
            borderwidth=0
        )
        self.lbl_xt.grid(row=9, column=0, padx=8, pady=(0, 6), sticky="w")
        self.lbl_xt.insert("1.0", "—")
        self.lbl_xt.config(state="disabled")

    def _build_animacion(self, parent):
        anim_f = make_section(parent, "Animacion masa-resorte", 2, 0, columnspan=3)

        self.canvas = tk.Canvas(
            anim_f,
            width=760,
            height=190,
            bg=BG2,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        self.canvas.pack(padx=10, pady=8)

        controles = tk.Frame(anim_f, bg=BG2)
        controles.pack(pady=(0, 8))

        self.btn_detener = tk.Button(
            controles,
            text="DETENER",
            bg=BG3,
            fg=ORANGE,
            font=FONT_BTN,
            relief="flat",
            cursor="hand2",
            activebackground=ORANGE,
            activeforeground=BG,
            padx=18,
            pady=7,
            command=self.detener_animacion
        )
        self.btn_detener.grid(row=0, column=0, padx=6)

        self.btn_repetir = tk.Button(
            controles,
            text="REPETIR",
            bg=BG3,
            fg=GREEN,
            font=FONT_BTN,
            relief="flat",
            cursor="hand2",
            activebackground=GREEN,
            activeforeground=BG,
            padx=18,
            pady=7,
            command=self.repetir_animacion
        )
        self.btn_repetir.grid(row=0, column=1, padx=6)

        self.dibujar_sistema(0)

    def _build_footer(self, parent):
        foot = tk.Frame(parent, bg=BG, pady=6)
        foot.grid(row=3, column=0, columnspan=3, sticky="ew")

        self.lbl_status = tk.Label(
            foot,
            text="Listo.",
            bg=BG,
            fg=MUTED,
            font=("Consolas", 9)
        )
        self.lbl_status.pack()

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Blue.Horizontal.TProgressbar",
            troughcolor=BG3,
            background=ACCENT,
            thickness=4
        )

        self.progress = ttk.Progressbar(
            foot,
            mode="indeterminate",
            length=520,
            style="Blue.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=(4, 4))

    def dibujar_sistema(self, x):
        self.canvas.delete("all")

        alto = 190
        pared_x = 80
        centro_y = alto // 2

        escala = 260
        masa_x = 390 + x * escala

        masa_w = 80
        masa_h = 55

        masa_x = max(180, min(640, masa_x))

        self.canvas.create_rectangle(
            pared_x - 15, 35,
            pared_x, 155,
            fill="#334155",
            outline="#94a3b8"
        )

        for y in range(40, 155, 15):
            self.canvas.create_line(
                pared_x - 15, y,
                pared_x, y - 12,
                fill="#64748b",
                width=1
            )

        self.canvas.create_line(
            40, 155,
            720, 155,
            fill="#475569",
            width=2
        )

        inicio_x = pared_x
        fin_x = masa_x - masa_w / 2
        vueltas = 12
        amp = 20

        puntos = []
        puntos.append((inicio_x, centro_y))

        largo = fin_x - inicio_x

        if largo < 40:
            largo = 40

        paso = largo / (vueltas * 2)

        for i in range(1, vueltas * 2):
            px = inicio_x + i * paso
            py = centro_y - amp if i % 2 == 0 else centro_y + amp
            puntos.append((px, py))

        puntos.append((fin_x, centro_y))

        for i in range(len(puntos) - 1):
            self.canvas.create_line(
                puntos[i][0], puntos[i][1],
                puntos[i + 1][0], puntos[i + 1][1],
                fill=ACCENT,
                width=3
            )

        self.canvas.create_rectangle(
            masa_x - masa_w / 2,
            centro_y - masa_h / 2,
            masa_x + masa_w / 2,
            centro_y + masa_h / 2,
            fill=ACCENT,
            outline="#bfdbfe",
            width=2
        )

        self.canvas.create_text(
            masa_x,
            centro_y,
            text="m",
            fill=BG,
            font=("Consolas", 18, "bold")
        )

        self.canvas.create_oval(
            masa_x - 30, centro_y + masa_h / 2 - 2,
            masa_x - 15, centro_y + masa_h / 2 + 13,
            fill="#0f172a",
            outline="#94a3b8"
        )

        self.canvas.create_oval(
            masa_x + 15, centro_y + masa_h / 2 - 2,
            masa_x + 30, centro_y + masa_h / 2 + 13,
            fill="#0f172a",
            outline="#94a3b8"
        )

        self.canvas.create_text(
            380,
            20,
            text=f"x(t) = {x:.4f}",
            fill=TEXT,
            font=("Consolas", 11, "bold")
        )

    def iniciar_animacion(self, Xt, t_inicio, t_final, pasos):
        t = sp.symbols("t", real=True)

        x_func = sp.lambdify(t, Xt, modules=["numpy"])

        self.anim_t_vals = np.linspace(t_inicio, t_final, pasos)
        self.anim_x_vals = np.real(x_func(self.anim_t_vals))

        self.anim_index = 0
        self.animando = True

        self.animar_frame()

    def animar_frame(self):
        if not self.animando:
            return

        if self.anim_index >= len(self.anim_x_vals):
            self.animando = False
            self.lbl_status.config(text="Animacion finalizada.")
            return

        x = self.anim_x_vals[self.anim_index]
        self.dibujar_sistema(x)

        self.anim_index += 1

        self.root.after(20, self.animar_frame)

    def detener_animacion(self):
        self.animando = False
        if hasattr(self, "lbl_status"):
            self.lbl_status.config(text="Animacion detenida.")

    def repetir_animacion(self):
        if len(self.anim_x_vals) == 0:
            self.lbl_status.config(text="Primero ejecuta una simulacion.")
            return

        self.anim_index = 0
        self.animando = True
        self.lbl_status.config(text="Repitiendo animacion...")
        self.animar_frame()

    def cargar_ejercicio(self, idx):
        ej = EJERCICIOS[idx]

        pares = [
            (self.e_m, ej["m"]),
            (self.e_b, ej["b"]),
            (self.e_k, ej["k"]),
            (self.e_x0, ej["x0"]),
            (self.e_v0, ej["v0"]),
            (self.e_t0, ej["t_inicio"]),
            (self.e_tf, ej["t_final"]),
            (self.e_pasos, ej["pasos"]),
        ]

        for entry, val in pares:
            entry.delete(0, tk.END)
            entry.insert(0, str(val))

        self.lbl_status.config(text=f"Cargado: {ej['nombre']}")
        self.detener_animacion()
        self.dibujar_sistema(ej["x0"])

    def limpiar_campos(self):
        for attr in ("e_m", "e_b", "e_k", "e_x0", "e_v0",
                     "e_t0", "e_tf", "e_pasos"):
            getattr(self, attr).delete(0, tk.END)

        self.lbl_status.config(text="Modo manual — ingresa los parametros.")
        self.detener_animacion()
        self.dibujar_sistema(0)

    def mostrar_solucion_texto(self, texto):
        self.lbl_xt.config(state="normal")
        self.lbl_xt.delete("1.0", tk.END)
        self.lbl_xt.insert("1.0", texto)
        self.lbl_xt.config(state="disabled")

    def simular(self):
        try:
            m = float(self.e_m.get())
            b = float(self.e_b.get())
            k = float(self.e_k.get())
            x0 = float(self.e_x0.get())
            v0 = float(self.e_v0.get())
            t_inicio = float(self.e_t0.get())
            t_final = float(self.e_tf.get())
            pasos = int(self.e_pasos.get())

        except ValueError:
            messagebox.showerror(
                "Error de entrada",
                "Revisa los valores ingresados.\nTodos deben ser numeros."
            )
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

        self.detener_animacion()

        tipo, disc, omega_n, zeta = clasificar_amortiguamiento(m, b, k)

        self.var_tipo.set(tipo)
        self.var_wn.set(f"{omega_n:.6f} rad/s")
        self.var_zeta.set(f"{zeta:.6f}")
        self.var_disc.set(f"{disc:.6f}")

        self.mostrar_solucion_texto("Calculando...")
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

            self.mostrar_solucion_texto(formatear_solucion(Xt))
            self.lbl_status.config(text="Generando grafica y animacion...")

            try:
                graficar_solucion(
                    Xt,
                    t_inicio=t_inicio,
                    t_final=t_final,
                    pasos=pasos,
                    titulo=titulo
                )

                plt.show(block=False)

                self.iniciar_animacion(
                    Xt,
                    t_inicio=t_inicio,
                    t_final=t_final,
                    pasos=pasos
                )

                self.lbl_status.config(text="Listo.")

            except Exception as e:
                messagebox.showerror("Error al graficar o animar", str(e))
                self.lbl_status.config(text="Error al graficar o animar.")

        threading.Thread(target=run, daemon=True).start()


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()