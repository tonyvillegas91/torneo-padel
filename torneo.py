import tkinter as tk
from tkinter import messagebox
from itertools import combinations
import random

# Variables globales
participantes = []
partidos = []
resultados = {}

# Función para registrar participantes
def registrar_participantes():
    equipo = entry_equipo.get().strip()
    if equipo and equipo not in participantes:
        participantes.append(equipo)
        lista_participantes.insert(tk.END, equipo)
        entry_equipo.delete(0, tk.END)
    else:
        messagebox.showwarning("Aviso", "Introduce un equipo válido o que no esté ya registrado.")

# Generar enfrentamientos
def generar_enfrentamientos():
    if len(participantes) != 4:
        messagebox.showerror("Error", "Debe haber exactamente 4 equipos para este formato.")
        return

    global partidos
    equipos = participantes[:]
    random.shuffle(equipos)  # Aleatorizar el orden de los equipos

    # Generar enfrentamientos asegurando que no se repitan equipos en el mismo turno
    partidos = [
        (equipos[0], equipos[1]),  # Pista 1
        (equipos[2], equipos[3]),  # Pista 2
        (equipos[0], equipos[2]),  # Pista 1
        (equipos[1], equipos[3]),  # Pista 2
        (equipos[0], equipos[3]),  # Pista 1
        (equipos[1], equipos[2]),  # Pista 2
    ]
    
    # Mostrar los enfrentamientos
    lista_partidos.delete(0, tk.END)
    for partido in partidos:
        lista_partidos.insert(tk.END, f"{partido[0]} vs {partido[1]}")

    crear_campos_resultados()
    messagebox.showinfo("Éxito", "¡Enfrentamientos generados correctamente!")

# Crear campos para registrar resultados
def crear_campos_resultados():
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    global entry_resultados
    entry_resultados = {}

    encabezado = ["Equipo 1", "Resultado 1", "Resultado 2", "Equipo 2"]
    for col, text in enumerate(encabezado):
        tk.Label(frame_resultados, text=text, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=5)

    for i, partido in enumerate(partidos):
        p1, p2 = partido
        tk.Label(frame_resultados, text=p1).grid(row=i + 1, column=0, padx=5, pady=5)
        entry_p1 = tk.Entry(frame_resultados, width=5)
        entry_p1.grid(row=i + 1, column=1, padx=5, pady=5)
        entry_p2 = tk.Entry(frame_resultados, width=5)
        entry_p2.grid(row=i + 1, column=2, padx=5, pady=5)
        tk.Label(frame_resultados, text=p2).grid(row=i + 1, column=3, padx=5, pady=5)

        entry_resultados[partido] = (entry_p1, entry_p2)

# Registrar resultados de los partidos
def registrar_resultados():
    global resultados
    resultados = {}
    try:
        for partido, (entry_p1, entry_p2) in entry_resultados.items():
            juegos_p1 = int(entry_p1.get())
            juegos_p2 = int(entry_p2.get())
            resultados[partido] = {"juegos_p1": juegos_p1, "juegos_p2": juegos_p2}
        messagebox.showinfo("Éxito", "¡Resultados registrados correctamente!")
    except ValueError:
        messagebox.showerror("Error", "Asegúrate de ingresar solo números en los campos de resultados.")

# Calcular clasificación
def calcular_clasificacion():
    if not resultados:
        messagebox.showerror("Error", "No se han registrado resultados aún.")
        return
    
    tabla = {p: {"puntos": 0, "juegos_diferencia": 0} for p in participantes}
    for partido, resultado in resultados.items():
        p1, p2 = partido
        juegos_p1, juegos_p2 = resultado["juegos_p1"], resultado["juegos_p2"]
        
        # Si hay empate, sumar 1 punto a cada equipo
        if juegos_p1 == juegos_p2:
            tabla[p1]["puntos"] += 1
            tabla[p2]["puntos"] += 1
        elif juegos_p1 > juegos_p2:
            tabla[p1]["puntos"] += 2
            tabla[p2]["puntos"] += 0
            tabla[p1]["juegos_diferencia"] += juegos_p1 - juegos_p2
            tabla[p2]["juegos_diferencia"] += juegos_p2 - juegos_p1
        else:
            tabla[p2]["puntos"] += 2
            tabla[p1]["puntos"] += 0
            tabla[p2]["juegos_diferencia"] += juegos_p2 - juegos_p1
            tabla[p1]["juegos_diferencia"] += juegos_p1 - juegos_p2
    
    mostrar_clasificacion(tabla)

# Mostrar clasificación final con criterio de desempate
def mostrar_clasificacion(tabla):
    clasificacion = sorted(tabla.items(), key=lambda x: (-x[1]["puntos"], -x[1]["juegos_diferencia"]))
    
    resultado_final.delete(1.0, tk.END)
    resultado_final.insert(tk.END, "--- Clasificación final ---\n")
    for i, (equipo, datos) in enumerate(clasificacion, start=1):
        resultado_final.insert(tk.END, f"{i}. {equipo}: {datos['puntos']} puntos, diferencia de juegos {datos['juegos_diferencia']}\n")

# Función para restablecer todo
def restablecer_torneo():
    global participantes, partidos, resultados
    participantes = []
    partidos = []
    resultados = {}

    # Limpiar la interfaz
    lista_participantes.delete(0, tk.END)
    lista_partidos.delete(0, tk.END)
    resultado_final.delete(1.0, tk.END)
    
    for widget in frame_resultados.winfo_children():
        widget.destroy()

    entry_equipo.delete(0, tk.END)
    messagebox.showinfo("Restablecer", "¡Torneo restablecido correctamente!")

# Ventana principal
root = tk.Tk()
root.title("Torneo de Pádel")



# Widgets para registrar participantes
tk.Label(root, text="Nombre del equipo:").pack()
entry_equipo = tk.Entry(root)
entry_equipo.pack()
tk.Button(root, text="Añadir equipo", command=registrar_participantes).pack()

lista_participantes = tk.Listbox(root, height=10, width=50)
lista_participantes.pack()

# Generar enfrentamientos
tk.Button(root, text="Generar enfrentamientos", command=generar_enfrentamientos).pack()
lista_partidos = tk.Listbox(root, height=10, width=50)
lista_partidos.pack()

# Frame para resultados
frame_resultados = tk.Frame(root)
frame_resultados.pack()

# Registrar resultados
tk.Button(root, text="Registrar resultados", command=registrar_resultados).pack()

# Mostrar clasificación final
tk.Button(root, text="Calcular clasificación", command=calcular_clasificacion).pack()
resultado_final = tk.Text(root, height=10, width=70)
resultado_final.pack()

# Botón para restablecer el torneo
tk.Button(root, text="Restablecer torneo", command=restablecer_torneo).pack()

root.mainloop()
