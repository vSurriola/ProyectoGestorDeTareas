import tkinter as tk
from tkinter import messagebox
from controllers.task_controller import TaskController

class TaskView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas Dinámico")
        self.root.geometry("600x550")
        self.root.configure(bg="#f0f4f7")

        self.controller = TaskController(self)

        header = tk.Label(root, text="Gestor de Tareas", font=("Helvetica", 18, "bold"), bg="#f0f4f7", fg="#333")
        header.pack(pady=10)

        main_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.task_listbox = tk.Listbox(main_frame, height=10, font=("Helvetica", 10), selectmode=tk.SINGLE)
        self.task_listbox.pack(padx=10, pady=10, fill="x")
        self.task_listbox.bind("<<ListboxSelect>>", self.on_select)

        form_frame = tk.Frame(main_frame, bg="#ffffff")
        form_frame.pack(padx=10, pady=10, fill="x")

        self.create_labeled_entry(form_frame, "Título:", 0)
        self.create_labeled_entry(form_frame, "Descripción:", 1)
        self.create_labeled_entry(form_frame, "Fecha (YYYY-MM-DD):", 2)
        self.create_labeled_entry(form_frame, "Prioridad:", 3)

        self.mark_done_var = tk.IntVar()
        self.mark_done_checkbox = tk.Checkbutton(main_frame, text="Marcar como completada", variable=self.mark_done_var, bg="#ffffff")
        self.mark_done_checkbox.pack()

        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Agregar", width=12, command=self.add_task, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Modificar", width=12, command=self.modify_task, bg="#2196F3", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Eliminar", width=12, command=self.delete_task, bg="#f44336", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Limpiar", width=12, command=self.clear_fields, bg="#9E9E9E", fg="white").grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="✔ Marcar como completada", width=25, command=self.mark_as_done, bg="#795548", fg="white").grid(row=1, column=0, columnspan=4, pady=10)

        self.update_task_list()

    def create_labeled_entry(self, parent, label_text, row):
        label = tk.Label(parent, text=label_text, bg="#ffffff", anchor="w")
        label.grid(row=row, column=0, sticky="w", pady=5)
        entry = tk.Entry(parent, width=40)
        entry.grid(row=row, column=1, padx=5, pady=5)

        if "Título" in label_text:
            self.title_entry = entry
        elif "Descripción" in label_text:
            self.desc_entry = entry
        elif "Fecha" in label_text:
            self.date_entry = entry
        elif "Prioridad" in label_text:
            self.priority_entry = entry

    def get_field_values(self):
        return (
            self.title_entry.get(),
            self.desc_entry.get(),
            self.date_entry.get(),
            self.priority_entry.get()
        )

    def update_task_list(self):
        self.task_listbox.delete(0, tk.END)
        for i, task in enumerate(self.controller.get_tasks()):
            check = "✔" if i in self.controller.get_completed() else ""
            self.task_listbox.insert(tk.END, f"{check} {task['titulo']} - {task['due_date']} ({task['prioridad']})")

    def on_select(self, event):
        try:
            index = self.task_listbox.curselection()[0]
            task = self.controller.get_tasks()[index]
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, task['titulo'])
            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, task['descripcion'])
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, task['due_date'])
            self.priority_entry.delete(0, tk.END)
            self.priority_entry.insert(0, task['prioridad'])
        except IndexError:
            pass

    def add_task(self):
        try:
            self.controller.add_task(*self.get_field_values())
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def modify_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.controller.modify_task(index, *self.get_field_values())
        except IndexError:
            messagebox.showerror("Error", "Selecciona una tarea para modificar")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.controller.delete_task(index)
        except IndexError:
            messagebox.showerror("Error", "Selecciona una tarea para eliminar")

    def mark_as_done(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.controller.mark_as_done(index)
        except IndexError:
            messagebox.showerror("Error", "Selecciona una tarea para marcar como completada")

    def clear_fields(self):
        self.title_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)
