from resolver_laplace import resolver_laplace
from graficador import graficar_solucion
import math

EJERCICIOS = [
    {
        "nombre": "Ejercicio 1",
        "m": 10,
        "b": 0.4,
        "k": 0.16,
        "x0": 0,
        "v0": 0,
        "step_time": 1,
        "initial_value": 0.025,
        "final_value": 0,
        "t_inicio": 0,
        "t_final": 300,
        "pasos": 600
    },
    {
        "nombre": "Ejercicio 2",
        "m": 4,
        "b": 0,
        "k": 16,
        "x0": 0,
        "v0": 0,
        "step_time": 1,
        "initial_value": 1,
        "final_value": 0,
        "t_inicio": 0,
        "t_final": 10,
        "pasos": 500
    },
    {
        "nombre": "Ejercicio 3",
        "m": 10,
        "b": 0.2,
        "k": 0.04,
        "x0": 0,
        "v0": 0,
        "step_time": 1,
        "initial_value": 0.025,
        "final_value": 0,
        "t_inicio": 0,
        "t_final": 300,
        "pasos": 600
    },
    {
        "nombre": "Ejercicio 4",
        "m": 150,
        "b": 4.5,
        "k": 0.03,
        "x0": 0,
        "v0": 0,
        "step_time": 1,
        "initial_value": 1,
        "final_value": 0.025,
        "t_inicio": 0,
        "t_final": 1000,
        "pasos": 800
    },
    {
        "nombre": "Ejercicio 5",
        "m": 50,
        "b": 2,
        "k": 0.02,
        "x0": 0,
        "v0": 0,
        "step_time": 1,
        "initial_value": 1,
        "final_value": 0.025,
        "t_inicio": 0,
        "t_final": 1000,
        "pasos": 800
    }
]

def clasificar_amortiguamiento(m, b, k):
    discriminante = b**2 - 4*m*k
    omega_n = math.sqrt(k / m)
    zeta = b / (2 * math.sqrt(m * k)) if b > 0 else 0

    if b == 0:
        tipo = "SIN amortiguamiento (oscilacion pura)"

    elif abs(discriminante) < 1e-9:
        tipo = "Amortiguamiento CRITICO"

    elif discriminante > 0:
        tipo = "SOBRE amortiguado"

    else:
        tipo = "SUB amortiguado"

    return tipo, discriminante, omega_n, zeta

def pedir_float(mensaje, minimo=None):
    while True:
        try:
            valor = float(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"El valor debe ser >= {minimo}")
                continue
            
            return valor

        except ValueError:
            print("Entrada invalida.")

def pedir_int(mensaje, minimo=1):
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"El valor debe ser >= {minimo}")
                continue
            
            return valor

        except ValueError:
            print("Entrada invalida.")

def ejecutar(
        m, b, k,
        x0, v0,
        step_time,
        initial_value,
        final_value,
        t_inicio,
        t_final,
        pasos,
        nombre="Simulacion"):

    tipo, disc, omega_n, zeta = clasificar_amortiguamiento(m, b, k)

    print("\n--------------------------------------------------")
    print(nombre)

    print("\nParametros del Sistema")
    print(f"m = {m} kg")
    print(f"b = {b}")
    print(f"k = {k} N/m")

    print("\nCondiciones Inicailes")
    print(f"x(0) = {x0}")
    print(f"x'(0) = {v0}")

    print("\nDatos Step")
    print(f"Step Time = {step_time}")
    print(f"Initial Value = {initial_value}")
    print(f"Final Value = {final_value}")

    print("\nValores Calculados")
    print(f"Frecuencia natural wn = {omega_n:.4f} rad/s")
    print(f"Factor amortiguamiento zeta = {zeta:.4f}")
    print(f"Discriminante = {disc:.6f}")
    print(f"Tipo = {tipo}")

    print("\Ecuacion Diferencial: \n")

    Xt = resolver_laplace(
        m, b, k,
        x0, v0,
        step_time,
        initial_value,
        final_value
    )

    print(f"x(t) = {Xt}")
    print("\nGrafica\n")

    titulo = (
        f"{nombre} | "
        f"{tipo} | "
        f"wn={omega_n:.3f} | "
        f"zeta={zeta:.3f}"
    )

    graficar_solucion(
        Xt,
        t_inicio=t_inicio,
        t_final=t_final,
        pasos=pasos,
        titulo=titulo
    )

def menu():

    print("\nParametros del Sistema")
    m = pedir_float("Masa m (kg): ",minimo=0.0001)
    b = pedir_float("Amortiguamiento b (>=0): ",minimo=0)
    k = pedir_float("Constante resorte k (N/m): ",minimo=0.0001)

    print("\nCondiciones Iniciales")
    x0 = pedir_float("Posicion inicial x(0): ")
    v0 = pedir_float("Velocidad inicial x'(0): ")

    print("\nDatos Step")
    step_time = pedir_float("Step Time: ",minimo=0)
    initial_value = pedir_float("Initial Value: ")
    final_value = pedir_float("Final Value: ")

    print("\nRango de la Grafica")
    t_inicio = pedir_float("Tiempo inicial: ")
    t_final = pedir_float("Tiempo final: ",minimo=t_inicio + 0.01)
    pasos = pedir_int("Numero de pasos: ",minimo=50)

    ejecutar(
        m, b, k,
        x0, v0,
        step_time,
        initial_value,
        final_value,
        t_inicio,
        t_final,
        pasos,
        nombre="Simulacion Ejercicio Extra"
    )

def main():
    while True:
        print("\n---------------------------------------------------------")
        print("Simulador Masa-Resorte - Transformada de Laplace")
        print("---------------------------------------------------------")

        print("1) Ejercicio 1")
        print("2) Ejercicio 2")
        print("3) Ejercicio 3")
        print("4) Ejercicio 4")
        print("5) Ejercicio 5")
        print("6) Ingresar ejercicio manualmente")
        print("7) Salir")
        print("---------------------------------------------------------")
        opcion = input("Seleccione una opcion: ").strip()

        if opcion in ('1', '2', '3', '4', '5'):
            ej = EJERCICIOS[int(opcion) - 1]
            ejecutar(
                ej['m'],
                ej['b'],
                ej['k'],

                ej['x0'],
                ej['v0'],

                ej['step_time'],
                ej['initial_value'],
                ej['final_value'],

                ej['t_inicio'],
                ej['t_final'],
                ej['pasos'],

                nombre=ej['nombre']
            )

        elif opcion == '6':
            menu()

        elif opcion == '7':
            print("\nCerrando programa")
            break

        else:
            print("\nOpcion invalida")

if __name__ == "__main__":
    main()
    