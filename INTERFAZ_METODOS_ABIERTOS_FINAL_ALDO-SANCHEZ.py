import tkinter as tk
from tkinter import ttk, messagebox
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np  

# Métodos de raíz (secante, bisección, Newton-Raphson)
def bisection_method(f, x, a, b, tol=1e-6, max_iter=100):
    if f.subs(x, a) * f.subs(x, b) >= 0:
        return None, "El intervalo no cumple las condiciones del método.", []
    
    iter_count = 0
    table_data = []
    
    while (b - a) / 2 > tol and iter_count < max_iter:
        c = (a + b) / 2
        f_c = f.subs(x, c)
        table_data.append((iter_count, c, f_c))
        
        if f_c == 0:
            return c, f"Raíz encontrada: {c}", table_data
        elif f.subs(x, a) * f_c < 0:
            b = c
        else:
            a = c
        iter_count += 1
    
    return c, f"Aproximación de la raíz: {c}", table_data

def secante_method(f, x, x0, x1, tol=1e-6, max_iter=100):
    iter_count = 0
    table_data = []
    
    while iter_count < max_iter:
        fx0, fx1 = f.subs(x, x0), f.subs(x, x1)
        if abs(fx1) < tol:
            return x1, f"Raíz encontrada: {x1}", table_data
        x2 = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        table_data.append((iter_count, x2, f.subs(x, x2)))
        x0, x1 = x1, x2
        iter_count += 1
    
    return x1, f"Aproximación de la raíz: {x1}", table_data

def newton_raphson_method(f, x, x0, tol=1e-6, max_iter=100):
    h = 1e-5
    iter_count = 0
    table_data = []
    
    while iter_count < max_iter:
        fx = f.subs(x, x0)
        if abs(fx) < tol:
            return x0, f"Raíz encontrada: {x0}", table_data
        dfx = (f.subs(x, x0 + h) - fx) / h
        x0 = x0 - fx / dfx
        table_data.append((iter_count, x0, f.subs(x, x0)))
        iter_count += 1
    
    return x0, f"Aproximación de la raíz: {x0}", table_data

# Función para calcular la raíz
def calcular_raiz():
    try:
        x = sp.symbols('x')
        expr = entry_funcion.get()
        a = float(entry_a.get())
        b = entry_b.get()
        
        if b == "":
            b = None
        else:
            b = float(b)
        
        tol = float(entry_umbral.get())
        max_iter = int(entry_max_iter.get())
        
        f = sp.sympify(expr)
        
        if tipo_metodo.get() == "Secante":
            raiz, mensaje, table_data = secante_method(f, x, a, b, tol, max_iter)
        elif tipo_metodo.get() == "Bisección":
            raiz, mensaje, table_data = bisection_method(f, x, a, b, tol, max_iter)
        elif tipo_metodo.get() == "Newton-Raphson":
            raiz, mensaje, table_data = newton_raphson_method(f, x, a, tol, max_iter)
        else:
            messagebox.showerror("Error", "Seleccione un método válido")
            return
        
        if raiz is None:
            messagebox.showerror("Error", mensaje)
        else:
            messagebox.showinfo("Resultado", mensaje)
            actualizar_tabla(table_data)
            graficar_funcion(f, x, table_data, raiz)
    except Exception as e:
        messagebox.showerror("Error", f"Entrada inválida: {e}")

# Actualización de la tabla
def actualizar_tabla(data):
    for row in tabla.get_children():
        tabla.delete(row)
    for d in data:
        tabla.insert("", "end", values=d)

# Función para graficar la función y marcar la raíz
def graficar_funcion(f, x, data, raiz):
    fig.clear()
    ax = fig.add_subplot(111)
    ax.grid(True, linestyle='--', linewidth=0.5)
    
    x_vals = np.linspace(-10, 10, 400)
    y_vals = [f.subs(x, val) for val in x_vals]
    
    ax.plot(x_vals, y_vals, label="Función")
    ax.plot(raiz, f.subs(x, raiz), 'ro', label=f"Raíz: {raiz:.4f}")
    ax.axhline(0, color='black', linewidth=0.8)
    ax.legend()
    canvas.draw()

# Configuración de la aplicación GUI
root = tk.Tk()
root.title("Calculadora de Raíces")

frame_top = tk.Frame(root, borderwidth=2, relief="solid")
frame_top.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

btn_funcion = tk.Button(frame_top, text="Función", relief="ridge")
btn_funcion.grid(row=0, column=0, padx=5, pady=5)
entry_funcion = tk.Entry(frame_top)
entry_funcion.grid(row=0, column=1, padx=5, pady=5)

btn_metodo = tk.Button(frame_top, text="Método", relief="ridge")
btn_metodo.grid(row=1, column=0, padx=5, pady=5)
tipo_metodo = ttk.Combobox(frame_top, values=["Bisección", "Secante", "Newton-Raphson"])
tipo_metodo.grid(row=1, column=1, padx=5, pady=5)

entry_a = tk.Entry(frame_top)
entry_a.grid(row=0, column=3, padx=5, pady=5)
tk.Label(frame_top, text="a", relief="ridge").grid(row=0, column=2, padx=5, pady=5)

entry_b = tk.Entry(frame_top)
entry_b.grid(row=1, column=3, padx=5, pady=5)
tk.Label(frame_top, text="b", relief="ridge").grid(row=1, column=2, padx=5, pady=5)

entry_umbral = tk.Entry(frame_top)
entry_umbral.grid(row=0, column=5, padx=5, pady=5)
tk.Label(frame_top, text="Umbral", relief="ridge").grid(row=0, column=4, padx=5, pady=5)

entry_max_iter = tk.Entry(frame_top)
entry_max_iter.grid(row=1, column=5, padx=5, pady=5)
tk.Label(frame_top, text="Max iter", relief="ridge").grid(row=1, column=4, padx=5, pady=5)

btn_calcular = tk.Button(frame_top, text="Calcular", command=calcular_raiz, relief="ridge")
btn_calcular.grid(row=0, column=6, rowspan=2, padx=5, pady=5)

frame_table_graph = tk.Frame(root, borderwidth=2, relief="solid")
frame_table_graph.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

columns = ("i", "c", "f(c)")
tabla = ttk.Treeview(frame_table_graph, columns=columns, show="headings")
for col in columns:
    tabla.heading(col, text=col)
    tabla.column(col, anchor="center", width=80)

tabla.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

style = ttk.Style()
style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")
style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

fig = plt.Figure(figsize=(8, 6), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_table_graph)
canvas.get_tk_widget().grid(row=0, column=1, padx=5, pady=5)

root.mainloop()
