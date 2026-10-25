# Laboratorio N°7- Informática II
# Alumnos: Eberle Javier - Iñiguez Agustin
# https://github.com/GlobHD/Labo7.git

import tkinter as tk
from tkinter import messagebox
import math 

# --- FUNCIONES DEL POLINOMIO ---
# coeficientes del polinomio de a6 a a0, por defecto es el que nos dieron en el laboratorio
coef = [0, 1, 0, -8, 0, 82, -25]

def f(x):
    """Evalúa el polinomio f(x) = -25 + 82x - 8x^3 + x^5"""# aca hacemos la funcion que evaluara el polinomio que nos dieron en el laboratorio
    resultado = 0
    for a in coef:# usamos horner para no tener que escribir cada potencia
        resultado = resultado * x + a
    return resultado

def df(x):
    """Evalúa la derivada analítica f'(x) = 82 - 24x^2 + 5x^4"""# aca hacemos la funcion que evaluara la derivada del polinomio
    grado = len(coef) - 1
    resultado = 0
    for i in range(grado):# la derivada de a*x^n es a*n*x^(n-1)
        resultado = resultado * x + coef[i] * (grado - i)
    return resultado

def calcular_cifras(es):# aca calculamos cuantas cifras significativas corresponden a un es (formula de teoria despejada)
    return int(math.floor(2 - math.log10(es / 0.5) + 1e-9))

# --- MÉTODOS NUMÉRICOS ---
def calcular_biseccion(xl, xu, es, max_iter):# aca hacemos la funcion que evaluara el metodo de biseccion
    if xl >= xu:
        return None, 0, 0, "Error: xl debe ser menor que xu."
    if f(xl) * f(xu) >= 0:
        return None, 0, 0, "Error: No hay cambio de signo en el intervalo." #aca hacemos la condicion que nos dice si hay cambio de signo en el intervalo
    
    xr = xl #igualamos el valor de xl a xr para que sea el punto medio del intervalo
    ea = 100.0
    for i in range(1, max_iter + 1):# aca hacemos un for que nos va a permitir iterar hasta el maximo de iteraciones que le pasemos como parametro
        xrold = xr
        xr = (xl + xu) / 2.0
        
        if i > 1 and xr != 0:# en la primera iteracion no hay un xr anterior real para comparar
            ea = abs((xr - xrold) / xr) * 100.0
            
        test = f(xl) * f(xr)# aca hacemos la condicion que nos dice si hay cambio de signo en el intervalo
        if test < 0:
            xu = xr
        elif test > 0:
            xl = xr
        else:
            ea = 0.0
            
        if ea < es:# aca hacemos la condicion que nos dice si el error aproximado es menor al error especificado
            return xr, i, ea, "Éxito"
            
    return xr, max_iter, ea, "Máximo de iteraciones alcanzado."

def calcular_newton(x0, es, max_iter):# aca hacemos la funcion que evaluara el metodo de newton raphson
    xr = x0
    ea = 100.0
    for i in range(1, max_iter + 1):# aca hacemos un for que nos va a permitir iterar hasta el maximo de iteraciones que le pasemos como parametro
        xrold = xr
        derivada = df(xr)#derivamos xr
        if derivada == 0:
            return None, i, ea, "Error: Derivada nula."
            
        xr = xr - f(xr) / derivada
        # aca hacemos la condicion que nos dice si el error aproximado es menor al error especificado
        if xr != 0:
            ea = abs((xr - xrold) / xr) * 100.0
        else:# si xr es 0 no podemos dividir, entonces el error es 0 solo si no se movio
            ea = 0.0 if xrold == 0 else 100.0
            
        if ea < es:
            return xr, i, ea, "Éxito"
            
    return xr, max_iter, ea, "Máximo de iteraciones alcanzado."

def calcular_secante(x_menos1, x0, es, max_iter):
    ea = 100.0# el ea es el error aproximado, que se inicializa en 100 para que entre al bucle
    xr = x0
    for i in range(1, max_iter + 1):
        f0 = f(x0)
        f_menos1 = f(x_menos1)
        
        if f0 - f_menos1 == 0:#que pasa si la diferencia de las funciones evaluadas en los puntos es cero, ya que no se puede dividir por cero
            return None, i, ea, "Error: División por cero en la secante."
            
        xr = x0 - f0 * (x_menos1 - x0) / (f_menos1 - f0)
        
        if xr != 0:
            ea = abs((xr - x0) / xr) * 100.0# aca hacemos la condicion que nos dice si el error aproximado es menor al error especificado
        else:
            ea = 0.0 if x0 == 0 else 100.0
            
        x_menos1 = x0
        x0 = xr
        
        if ea < es:
            return xr, i, ea, "Éxito"
            
    return xr, max_iter, ea, "Máximo de iteraciones alcanzado."

# --- DERIVADA ---
def calcular_derivada(x, h):# aca hacemos la funcion que calcula la derivada con diferencia finita centrada
    return (f(x + h) - f(x - h)) / (2 * h)

# --- SISTEMA DE ECUACIONES (GAUSS) ---
def resolver_gauss(A, b, pivoteo):# aca hacemos la funcion que resuelve el sistema por eliminacion de gauss, con o sin pivoteo parcial
    n = len(b)
    A = [fila[:] for fila in A]# hacemos copias para no modificar los valores que escribio el usuario
    b = b[:]

    # eliminacion hacia adelante
    for k in range(n - 1):
        if pivoteo:
            # buscamos la fila con el mayor valor absoluto en la columna k y la intercambiamos
            fila_max = k
            for r in range(k + 1, n):
                if abs(A[r][k]) > abs(A[fila_max][k]):
                    fila_max = r
            if fila_max != k:
                A[k], A[fila_max] = A[fila_max], A[k]
                b[k], b[fila_max] = b[fila_max], b[k]

        if abs(A[k][k]) < 1e-12:# aca detectamos el pivote nulo
            if pivoteo:
                return None, "Error: La matriz es singular."
            return None, "Error: Pivote nulo en la fila " + str(k + 1) + ". Pruebe con pivoteo parcial."

        for i in range(k + 1, n):
            factor = A[i][k] / A[k][k]
            for j in range(k, n):
                A[i][j] = A[i][j] - factor * A[k][j]
            b[i] = b[i] - factor * b[k]

    if abs(A[n - 1][n - 1]) < 1e-12:# el ultimo pivote tambien puede ser nulo
        if pivoteo:
            return None, "Error: La matriz es singular."
        return None, "Error: Pivote nulo en la fila " + str(n) + ". Pruebe con pivoteo parcial."

    # sustitucion hacia atras
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        suma = 0
        for j in range(i + 1, n):
            suma = suma + A[i][j] * x[j]
        x[i] = (b[i] - suma) / A[i][i]
    return x, "Éxito"

# --- LÓGICA DE LA INTERFAZ ---
def leer_numero(entry, nombre, entero=False):# aca leemos un campo y avisamos si esta vacio o no es un numero
    texto = entry.get().strip().replace(",", ".")
    if texto == "":
        raise ValueError("El campo '" + nombre + "' está vacío.")
    try:
        if entero:
            return int(texto)
        return float(texto)
    except ValueError:
        raise ValueError("El campo '" + nombre + "' no es un número válido.")

def escribir(entry, texto):# aca escribimos en un entry aunque sea de solo lectura
    estado = str(entry.cget("state"))
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, texto)
    entry.config(state=estado)

def leer_coeficientes():# aca leemos los coeficientes a6..a0 y los guardamos en la lista coef
    global coef
    nuevos = []
    for i in range(7):
        nuevos.append(leer_numero(entries_coef[i], "a" + str(6 - i)))
    if all(a == 0 for a in nuevos):
        raise ValueError("El polinomio es nulo, ingrese algún coeficiente distinto de 0.")
    coef = nuevos

def valores_prueba_coef():
    for i, valor in enumerate([0, 1, 0, -8, 0, 82, -25]):
        escribir(entries_coef[i], str(valor))
    actualizar_metodo()

def borrar_coef():
    for e in entries_coef:
        escribir(e, "")

def actualizar_metodo():# aca cambiamos las etiquetas y ponemos los valores de prueba segun el metodo elegido
    metodo = var_metodo.get()
    entry_xu.config(state="normal")
    if metodo == "Bisección":
        label_xl.config(text="xl:")
        label_xu.config(text="xu:")
        escribir(entry_xl, "0")
        escribir(entry_xu, "1")
    elif metodo == "Newton-Raphson":
        label_xl.config(text="x0:")
        label_xu.config(text="")
        escribir(entry_xl, "0")
        escribir(entry_xu, "")
        entry_xu.config(state="disabled")# newton solo usa un valor inicial
    else:
        label_xl.config(text="x-1:")
        label_xu.config(text="x0:")
        escribir(entry_xl, "-1")
        escribir(entry_xu, "0")

def ejecutar_calculo_raiz():
    for e in (entry_res_raiz, entry_res_iter, entry_res_ea, entry_res_f):
        escribir(e, "")
    try:
        leer_coeficientes()

        # Validar y obtener criterio de parada
        if var_criterio.get() == "es":
            es = leer_numero(entry_es, "εs (%)")
            if es <= 0:
                raise ValueError("εs debe ser mayor que 0.")
            cifras = calcular_cifras(es)
        else:
            cifras = leer_numero(entry_cifras, "Cifras signif.", True)
            if cifras < 1:
                raise ValueError("Las cifras significativas deben ser al menos 1.")
            es = 0.5 * (10 ** (2 - cifras))
            
        max_iter = leer_numero(entry_max_iter, "Máx. iter.", True)
        if max_iter < 1:
            raise ValueError("El máximo de iteraciones debe ser al menos 1.")
        metodo = var_metodo.get()
        
        # Ejecutar método seleccionado
        if metodo == "Bisección":
            xl = leer_numero(entry_xl, "xl")
            xu = leer_numero(entry_xu, "xu")
            raiz, iters, ea, msg = calcular_biseccion(xl, xu, es, max_iter)
        elif metodo == "Newton-Raphson":
            x0 = leer_numero(entry_xl, "x0") # Reutilizamos campo
            raiz, iters, ea, msg = calcular_newton(x0, es, max_iter)
        elif metodo == "Secante":
            x_menos1 = leer_numero(entry_xl, "x-1") # Reutilizamos campo
            x0 = leer_numero(entry_xu, "x0")       # Reutilizamos campo
            raiz, iters, ea, msg = calcular_secante(x_menos1, x0, es, max_iter)
            
        # Mostrar resultados
        if raiz is not None:
            formato = f".{cifras}g"
            entry_res_raiz.config(state="normal")
            entry_res_raiz.delete(0, tk.END)
            entry_res_raiz.insert(0, format(raiz, formato))
            entry_res_raiz.config(state="readonly")
            
            entry_res_iter.config(state="normal")
            entry_res_iter.delete(0, tk.END)
            entry_res_iter.insert(0, str(iters))
            entry_res_iter.config(state="readonly")
            
            entry_res_ea.config(state="normal")
            entry_res_ea.delete(0, tk.END)
            entry_res_ea.insert(0, f"{ea:.4f}")
            entry_res_ea.config(state="readonly")
            
            entry_res_f.config(state="normal")
            entry_res_f.delete(0, tk.END)
            entry_res_f.insert(0, format(f(raiz), ".4e"))
            entry_res_f.config(state="readonly")
            
            if msg != "Éxito":
                messagebox.showwarning("Aviso", msg)
        else:
            messagebox.showerror("Error", msg)
            
    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))

def ejecutar_derivada():
    escribir(entry_res_deriv, "")
    try:
        leer_coeficientes()
        x = leer_numero(entry_x_deriv, "x0")
        h = leer_numero(entry_h_deriv, "dx")
        if h == 0:
            raise ValueError("El paso dx no puede ser 0.")
        escribir(entry_res_deriv, format(calcular_derivada(x, h), ".6g"))
    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))

def valores_prueba_sistema():
    A = [[2, 2, 1, -1], [2, -2, 6, -4], [2, 2, 1, 1], [1, 5, -4, -2]]
    b = [5, 0, 13, -9]
    for i in range(4):
        for j in range(4):
            escribir(entries_A[i][j], str(A[i][j]))
        escribir(entries_b[i], str(b[i]))

def borrar_sistema():
    for i in range(4):
        for j in range(4):
            escribir(entries_A[i][j], "")
        escribir(entries_b[i], "")
        escribir(entries_x[i], "")

def ejecutar_gauss():
    for e in entries_x:
        escribir(e, "")
    try:
        A = []
        for i in range(4):
            fila = []
            for j in range(4):
                fila.append(leer_numero(entries_A[i][j], "A[" + str(i + 1) + "][" + str(j + 1) + "]"))
            A.append(fila)
        b = []
        for i in range(4):
            b.append(leer_numero(entries_b[i], "b[" + str(i + 1) + "]"))
    except ValueError as e:
        messagebox.showerror("Error de entrada", str(e))
        return

    x, msg = resolver_gauss(A, b, var_pivoteo.get() == "con")
    if x is None:
        messagebox.showerror("Error", msg)
    else:
        for i in range(4):
            escribir(entries_x[i], format(x[i], ".6g"))

# --- INTERFAZ GRÁFICA (GUI) ---
ventana = tk.Tk()
ventana.title("Laboratorio VI.1 - Cálculo numérico")
ventana.geometry("850x680")

# Marco para los coeficientes del polinomio
frame_pol = tk.LabelFrame(ventana, text="Coeficientes del polinomio", padx=10, pady=5)
frame_pol.pack(fill="x", padx=10, pady=5)

entries_coef = []
for i in range(7):
    tk.Label(frame_pol, text="a" + str(6 - i)).grid(row=1, column=i)
    e = tk.Entry(frame_pol, width=6, justify="center")
    e.grid(row=0, column=i, padx=3)
    entries_coef.append(e)
tk.Button(frame_pol, text="Borrar", command=borrar_coef).grid(row=0, column=8, padx=10)
tk.Button(frame_pol, text="Valores de prueba", command=valores_prueba_coef).grid(row=1, column=8, padx=10)

# Marco para Cálculo de una raíz
frame_raiz = tk.LabelFrame(ventana, text="Cálculo de una raíz", padx=10, pady=10)
frame_raiz.pack(fill="x", padx=10, pady=5)

# Selección de Método
var_metodo = tk.StringVar(value="Bisección")
tk.Label(frame_raiz, text="Método:").grid(row=0, column=0, sticky="e")
tk.Radiobutton(frame_raiz, text="Bisección", variable=var_metodo, value="Bisección", command=actualizar_metodo).grid(row=0, column=1)
tk.Radiobutton(frame_raiz, text="Newton-Raphson", variable=var_metodo, value="Newton-Raphson", command=actualizar_metodo).grid(row=0, column=2)
tk.Radiobutton(frame_raiz, text="Secante", variable=var_metodo, value="Secante", command=actualizar_metodo).grid(row=0, column=3)

# Valores iniciales
label_xl = tk.Label(frame_raiz, text="xl:")
label_xl.grid(row=1, column=0, sticky="e", pady=5)
entry_xl = tk.Entry(frame_raiz, width=10)
entry_xl.grid(row=1, column=1, sticky="w")

label_xu = tk.Label(frame_raiz, text="xu:")
label_xu.grid(row=1, column=2, sticky="e")
entry_xu = tk.Entry(frame_raiz, width=10)
entry_xu.grid(row=1, column=3, sticky="w")

# Criterio de parada
var_criterio = tk.StringVar(value="es")
tk.Radiobutton(frame_raiz, text="εs (%):", variable=var_criterio, value="es").grid(row=2, column=0, sticky="e")
entry_es = tk.Entry(frame_raiz, width=8)
entry_es.grid(row=2, column=1, sticky="w")
entry_es.insert(0, "0.5")

tk.Radiobutton(frame_raiz, text="Cifras signif.:", variable=var_criterio, value="cifras").grid(row=2, column=2, sticky="e")
entry_cifras = tk.Entry(frame_raiz, width=8)
entry_cifras.grid(row=2, column=3, sticky="w")
entry_cifras.insert(0, "4")

tk.Label(frame_raiz, text="Máx. iter.:").grid(row=2, column=4, sticky="e")
entry_max_iter = tk.Entry(frame_raiz, width=8)
entry_max_iter.grid(row=2, column=5, sticky="w")
entry_max_iter.insert(0, "100")

# Botón Calcular
tk.Button(frame_raiz, text="Calcular", command=ejecutar_calculo_raiz).grid(row=1, column=4, columnspan=2, padx=10)

# Resultados
tk.Label(frame_raiz, text="Raíz:").grid(row=0, column=6, sticky="e")
entry_res_raiz = tk.Entry(frame_raiz, width=15, state="readonly")
entry_res_raiz.grid(row=0, column=7)

tk.Label(frame_raiz, text="Iteraciones:").grid(row=1, column=6, sticky="e")
entry_res_iter = tk.Entry(frame_raiz, width=15, state="readonly")
entry_res_iter.grid(row=1, column=7)

tk.Label(frame_raiz, text="εa (%):").grid(row=2, column=6, sticky="e")
entry_res_ea = tk.Entry(frame_raiz, width=15, state="readonly")
entry_res_ea.grid(row=2, column=7)

tk.Label(frame_raiz, text="f(raíz):").grid(row=3, column=6, sticky="e")
entry_res_f = tk.Entry(frame_raiz, width=15, state="readonly")
entry_res_f.grid(row=3, column=7)

# Marco para la derivada
frame_deriv = tk.LabelFrame(ventana, text="Cálculo de la derivada primera (diferencia centrada)", padx=10, pady=5)
frame_deriv.pack(fill="x", padx=10, pady=5)

tk.Label(frame_deriv, text="x0:").grid(row=0, column=0)
entry_x_deriv = tk.Entry(frame_deriv, width=8)
entry_x_deriv.grid(row=0, column=1)
entry_x_deriv.insert(0, "1")

tk.Label(frame_deriv, text="dx:").grid(row=0, column=2, padx=(10, 0))
entry_h_deriv = tk.Entry(frame_deriv, width=8)
entry_h_deriv.grid(row=0, column=3)
entry_h_deriv.insert(0, "0.13")

tk.Button(frame_deriv, text="Calcular", command=ejecutar_derivada).grid(row=0, column=4, padx=15)
tk.Label(frame_deriv, text="Derivada f'(x0):").grid(row=0, column=5)
entry_res_deriv = tk.Entry(frame_deriv, width=15, state="readonly")
entry_res_deriv.grid(row=0, column=6, padx=5)

# Marco para el sistema de ecuaciones
frame_sis = tk.LabelFrame(ventana, text="Resolución de un sistema de 4 ecuaciones (eliminación gaussiana)", padx=10, pady=5)
frame_sis.pack(fill="x", padx=10, pady=5)

for j, nombre in enumerate(["x1", "x2", "x3", "x4", "", "b"]):
    tk.Label(frame_sis, text=nombre).grid(row=0, column=j)

entries_A = []
entries_b = []
for i in range(4):
    fila = []
    for j in range(4):
        e = tk.Entry(frame_sis, width=6, justify="center")
        e.grid(row=i + 1, column=j, padx=2, pady=2)
        fila.append(e)
    entries_A.append(fila)
    tk.Label(frame_sis, text="|").grid(row=i + 1, column=4)
    e = tk.Entry(frame_sis, width=6, justify="center")
    e.grid(row=i + 1, column=5, padx=2, pady=2)
    entries_b.append(e)

var_pivoteo = tk.StringVar(value="sin")
tk.Radiobutton(frame_sis, text="Sin pivoteo", variable=var_pivoteo, value="sin").grid(row=1, column=6, sticky="w", padx=15)
tk.Radiobutton(frame_sis, text="Con pivoteo parcial", variable=var_pivoteo, value="con").grid(row=2, column=6, sticky="w", padx=15)
tk.Button(frame_sis, text="Calcular", width=12, command=ejecutar_gauss).grid(row=3, column=6)
tk.Button(frame_sis, text="Borrar", width=12, command=borrar_sistema).grid(row=4, column=6)
tk.Button(frame_sis, text="Valores de prueba", width=12, command=valores_prueba_sistema).grid(row=5, column=6)

entries_x = []
for i in range(4):
    tk.Label(frame_sis, text="x" + str(i + 1) + " =").grid(row=i + 1, column=7, padx=(20, 0))
    e = tk.Entry(frame_sis, width=14, state="readonly")
    e.grid(row=i + 1, column=8)
    entries_x.append(e)

# Valores de prueba iniciales
valores_prueba_coef()
valores_prueba_sistema()

# Falta el punto 4 (integral con Simpson 1/3 compuesta)

ventana.mainloop()