# Laboratorio N°7- Informática II
# Alumnos: Eberle Javier - Iñiguez Agustin
# https://github.com/GlobHD/Labo7.git
import tkinter as tk
from tkinter import messagebox
import math #Javo fijate si te deja usar la biblioteca, a mi me aparece como si no la tuviera instalada, si no la tenes instalada, podes usar el metodo de biseccion que no necesita la biblioteca math

# --- FUNCIONES DEL POLINOMIO ---
def f(x):
    """Evalúa el polinomio f(x) = -25 + 82x - 8x^3 + x^5"""# aca hacemos la funcion que evaluara el polinomio que nos dieron en el laboratorio
    return -25 + 82*x - 8*(x**3) + (x**5)

def df(x):
    """Evalúa la derivada analítica f'(x) = 82 - 24x^2 + 5x^4"""# aca hacemos la funcion que evaluara la derivada del polinomio
    return 82 - 24*(x**2) + 5*(x**4)

# --- MÉTODOS NUMÉRICOS ---
def calcular_biseccion(xl, xu, es, max_iter):# aca hacemos la funcion que evaluara el metodo de biseccion
    if f(xl) * f(xu) >= 0:
        return None, 0, 0, "Error: No hay cambio de signo en el intervalo." #aca hacemos la condicion que nos dice si hay cambio de signo en el intervalo
    
    xr = xl #igualamos el valor de xl a xr para que sea el punto medio del intervalo
    ea = 100.0
    for i in range(1, max_iter + 1):# aca hacemos un for que nos va a permitir iterar hasta el maximo de iteraciones que le pasemos como parametro
        xrold = xr
        xr = (xl + xu) / 2.0
        
        if xr != 0:
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
            
        if ea < es:
            return xr, i, ea, "Éxito"
            
    return xr, max_iter, ea, "Máximo de iteraciones alcanzado."

def calcular_secante(x_menos1, x0, es, max_iter):
    ea = 100.0# el ea es el error aproximado, que se inicializa en 100 para que entre al bucle
    for i in range(1, max_iter + 1):
        f0 = f(x0)
        f_menos1 = f(x_menos1)
        
        if f0 - f_menos1 == 0:#que pasa si la diferencia de las funciones evaluadas en los puntos es cero, ya que no se puede dividir por cero
            return None, i, ea, "Error: División por cero en la secante."
            
        xr = x0 - f0 * (x_menos1 - x0) / (f_menos1 - f0)
        
        if xr != 0:
            ea = abs((xr - x0) / xr) * 100.0# aca hacemos la condicion que nos dice si el error aproximado es menor al error especificado
            
        x_menos1 = x0
        x0 = xr
        
        if ea < es:
            return xr, i, ea, "Éxito"
            
    return xr, max_iter, ea, "Máximo de iteraciones alcanzado."

# --- LÓGICA DE LA INTERFAZ ---
def ejecutar_calculo_raiz():
    try:
        # Validar y obtener criterio de parada
        if var_criterio.get() == "es":
            es = float(entry_es.get())
            cifras = None
        else:
            cifras = int(entry_cifras.get())
            es = 0.5 * (10 ** (2 - cifras))
            
        max_iter = int(entry_max_iter.get())
        metodo = var_metodo.get()
        
        # Ejecutar método seleccionado
        if metodo == "Bisección":
            xl = float(entry_xl.get())
            xu = float(entry_xu.get())
            raiz, iters, ea, msg = calcular_biseccion(xl, xu, es, max_iter)
        elif metodo == "Newton-Raphson":
            x0 = float(entry_xl.get()) # Reutilizamos campo
            raiz, iters, ea, msg = calcular_newton(x0, es, max_iter)
        elif metodo == "Secante":
            x_menos1 = float(entry_xl.get()) # Reutilizamos campo
            x0 = float(entry_xu.get())       # Reutilizamos campo
            raiz, iters, ea, msg = calcular_secante(x_menos1, x0, es, max_iter)
            
        # Mostrar resultados
        if raiz is not None:
            formato = f".{cifras}g" if cifras else ".6g"
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
            
    except ValueError:
        messagebox.showerror("Error de entrada", "Asegúrese de ingresar valores numéricos válidos en todos los campos requeridos.")

# --- INTERFAZ GRÁFICA (GUI) ---
ventana = tk.Tk()
ventana.title("Laboratorio VI.1 - Cálculo numérico")
ventana.geometry("750x600")

# Marco para Cálculo de una raíz
frame_raiz = tk.LabelFrame(ventana, text="Cálculo de una raíz", padx=10, pady=10)
frame_raiz.pack(fill="x", padx=10, pady=5)

# Selección de Método
var_metodo = tk.StringVar(value="Bisección")
tk.Label(frame_raiz, text="Método:").grid(row=0, column=0, sticky="e")
tk.Radiobutton(frame_raiz, text="Bisección", variable=var_metodo, value="Bisección").grid(row=0, column=1)
tk.Radiobutton(frame_raiz, text="Newton-Raphson", variable=var_metodo, value="Newton-Raphson").grid(row=0, column=2)
tk.Radiobutton(frame_raiz, text="Secante", variable=var_metodo, value="Secante").grid(row=0, column=3)

# Valores iniciales
tk.Label(frame_raiz, text="xl / x0 / x-1:").grid(row=1, column=0, sticky="e", pady=5)
entry_xl = tk.Entry(frame_raiz, width=10)
entry_xl.grid(row=1, column=1, sticky="w")
entry_xl.insert(0, "0")

tk.Label(frame_raiz, text="xu / x0:").grid(row=1, column=2, sticky="e")
entry_xu = tk.Entry(frame_raiz, width=10)
entry_xu.grid(row=1, column=3, sticky="w")
entry_xu.insert(0, "1")

# Criterio de parada
var_criterio = tk.StringVar(value="es")
tk.Radiobutton(frame_raiz, text="εs (%):", variable=var_criterio, value="es").grid(row=2, column=0, sticky="e")
entry_es = tk.Entry(frame_raiz, width=8)
entry_es.grid(row=2, column=1, sticky="w")
entry_es.insert(0, "0.5")

tk.Radiobutton(frame_raiz, text="Cifras signif.:", variable=var_criterio, value="cifras").grid(row=2, column=2, sticky="e")
entry_cifras = tk.Entry(frame_raiz, width=8)
entry_cifras.grid(row=2, column=3, sticky="w")

tk.Label(frame_raiz, text="Máx. iter.:").grid(row=2, column=4, sticky="e")
entry_max_iter = tk.Entry(frame_raiz, width=8)
entry_max_iter.grid(row=2, column=5, sticky="w")
entry_max_iter.insert(0, "100")

# Botón Calcular
tk.Button(frame_raiz, text="Calcular", command=ejecutar_calculo_raiz).grid(row=1, column=4, rowspan=2, padx=10)

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

ventana.mainloop()