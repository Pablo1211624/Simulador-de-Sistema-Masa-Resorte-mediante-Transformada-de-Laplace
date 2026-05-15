# Simulador Masa-Resorte con Transformada de Laplace

Aplicación de escritorio desarrollada en Python para simular el comportamiento de un sistema masa-resorte-amortiguador usando la Transformada de Laplace.

El programa permite ingresar los parámetros físicos del sistema, resolver la ecuación diferencial, clasificar el tipo de amortiguamiento, visualizar la solución matemática y observar una animación del movimiento de la masa conectada a un resorte.

---

## Vista general

Este proyecto resuelve sistemas de la forma:

m x''(t) + b x'(t) + k x(t) = 0

donde:

m es la masa.
b es el coeficiente de amortiguamiento.
k es la constante del resorte.
x(0) es la posición inicial.
x'(0) es la velocidad inicial.

La solución se obtiene mediante Transformada de Laplace y se visualiza mediante una interfaz gráfica construida con Tkinter.

Características principales
Interfaz gráfica de escritorio con Tkinter.
Resolución simbólica usando SymPy.
Evaluación numérica usando NumPy.
Gráfica de la solución x(t) con Matplotlib.
Animación visual del sistema masa-resorte.
Ejercicios precargados.
Modo manual para ingresar parámetros personalizados.
Clasificación automática del tipo de amortiguamiento:
Sin amortiguamiento.
Subamortiguado.
Sobreamortiguado.
Amortiguamiento crítico.
Cálculo de:
Frecuencia natural.
Factor de amortiguamiento.
Discriminante del sistema.
Solución simbólica x(t).


## Tecnologías utilizadas
Python
Tkinter
SymPy
NumPy
Matplotlib
PyInstaller