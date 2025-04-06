import json
from models.task import Task
from datetime import datetime

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, titulo, descripcion, due_date, prioridad):
        Task.validate_date(due_date)
        new_task = Task(titulo, descripcion, due_date, prioridad)
        self.tasks.append(new_task.to_dict())
        self.save_tasks()

    def modify_task(self, index, titulo=None, descripcion=None, due_date=None, prioridad=None):
        if 0 <= index < len(self.tasks):
            if titulo:
                self.tasks[index]["titulo"] = titulo
            if descripcion:
                self.tasks[index]["descripcion"] = descripcion
            if due_date:
                Task.validate_date(due_date)
                self.tasks[index]["due_date"] = due_date
            if prioridad:
                self.tasks[index]["prioridad"] = prioridad
            self.save_tasks()
        else:
            raise IndexError("Tarea fuera de rango.")

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
        else:
            raise IndexError("Tarea fuera de rango.")

# Añadir método estático a Task
Task.validate_date = staticmethod(lambda date: datetime.strptime(date, "%Y-%m-%d"))