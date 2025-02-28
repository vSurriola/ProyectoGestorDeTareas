import tkinter as tk
from tkinter import ttk, messagebox

# Función para cerrar la pantalla de inicio y abrir la ventana principal
def abrir_principal():
    splash.destroy()
    
    # Ventana principal
    root = tk.Tk()
    root.title("Gestor de Tareas")
    root.geometry("400x500")

    # Lista de tareas
    tareas = []

    # Función para agregar una tarea
    def agregar_tarea():
        tarea = entry_tarea.get()
        if tarea:
            tareas.append(tarea)
            actualizar_lista()
            entry_tarea.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "No puedes agregar una tarea vacía")

    # Función para eliminar una tarea
    def eliminar_tarea():
        try:
            seleccion = lista_tareas.curselection()[0]
            tareas.pop(seleccion)
            actualizar_lista()
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")

    # Función para modificar una tarea
    def modificar_tarea():
        try:
            seleccion = lista_tareas.curselection()[0]
            nueva_tarea = entry_tarea.get()
            if nueva_tarea:
                tareas[seleccion] = nueva_tarea
                actualizar_lista()
                entry_tarea.delete(0, tk.END)
            else:
                messagebox.showwarning("Advertencia", "Escribe una nueva tarea antes de modificar")
        except IndexError:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para modificar")

    # Función para actualizar la lista de tareas
    def actualizar_lista():
        lista_tareas.delete(0, tk.END)
        for tarea in tareas:
            lista_tareas.insert(tk.END, tarea)

    # Widgets de la interfaz
    lbl_titulo = tk.Label(root, text="Gestor de Tareas", font=("Arial", 14, "bold"))
    lbl_titulo.pack(pady=10)

    entry_tarea = tk.Entry(root, width=40)
    entry_tarea.pack(pady=5)

    frame_botones = tk.Frame(root)
    frame_botones.pack()

    btn_agregar = tk.Button(frame_botones, text="Agregar", command=agregar_tarea, width=10)
    btn_agregar.grid(row=0, column=0, padx=5, pady=5)

    btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=eliminar_tarea, width=10)
    btn_eliminar.grid(row=0, column=1, padx=5, pady=5)

    btn_modificar = tk.Button(frame_botones, text="Modificar", command=modificar_tarea, width=10)
    btn_modificar.grid(row=0, column=2, padx=5, pady=5)

    lista_tareas = tk.Listbox(root, width=50, height=15)
    lista_tareas.pack(pady=10)

    root.mainloop()

# --------- PANTALLA DE INICIO ---------
splash = tk.Tk()
splash.title("Cargando...")
splash.geometry("300x200")
splash.configure(bg="lightblue")

lbl = tk.Label(splash, text="Gestor de Tareas", font=("Arial", 16, "bold"), bg="lightblue")
lbl.pack(pady=20)

progress = ttk.Progressbar(splash, orient="horizontal", length=200, mode="determinate")
progress.pack(pady=20)

# Simulación de carga
def cargar():
    for _ in range(5):
        splash.update_idletasks()
        progress["value"] += 20
        splash.after(500)
    abrir_principal()

splash.after(1000, cargar)
splash.mainloop()
