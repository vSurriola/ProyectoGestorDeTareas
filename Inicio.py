import json
from datetime import datetime

# Clase que representa una tarea
class Task:
    def __init__(self, titulo, descripcion, due_date, prioridad):
        self.titulo = titulo
        self.descripcion = descripcion
        self.due_date = due_date  # Fecha en formato YYYY-MM-DD
        self.prioridad = prioridad

    def to_dict(self):
        # Convierte la tarea en un diccionario para  almacenamiento en JSON
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "due_date": self.due_date,
            "prioridad": self.prioridad
        }

# Clase para la gestión de tareas
class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()  # Carga las tareas desde el archivo JSON

    def load_tasks(self):
        # Carga las tareas desde un archivo JSON, si no existe devuelve una lista vacía
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        # Guarda las tareas en el archivo JSON
        with open(self.filename, "w") as file:
            json.dump(self.tasks, file, indent=4)

    def add_task(self, titulo, descripcion, due_date, prioridad):
        # Agrega una nueva tarea a la lista y la guarda en el archivo
        try:
            datetime.strptime(due_date, "%Y-%m-%d")  # Validación de formato de fecha
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD.")
        
        new_task = Task(titulo, descripcion, due_date, prioridad)
        self.tasks.append(new_task.to_dict())
        self.save_tasks()

    def modify_task(self, index, titulo=None, descripcion=None, due_date=None, prioridad=None):
        # Modifica una tarea existente en base a su indice en la lista
        if 0 <= index < len(self.tasks):
            if titulo:
                self.tasks[index]["titulo"] = titulo
            if descripcion:
                self.tasks[index]["descripcion"] = descripcion
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                    self.tasks[index]["due_date"] = due_date
                except ValueError:
                    raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            if prioridad:
                self.tasks[index]["prioridad"] = prioridad
            self.save_tasks()
        else:
            raise IndexError("Task index out of range.")

    def delete_task(self, index):
        # Elimina una tarea por su indice y guarda los cambios
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_tasks()
        else:
            raise IndexError("Task index out of range.")

# Test unitarios para verificar la funcionalidad
import unittest

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        # Configuración inicial: crea una instancia de TaskManager con un archivo de prueba
        self.task_manager = TaskManager("test_tasks.json")
        self.task_manager.tasks = []  # Reseteo de tareas

    def test_add_task(self):
        # Prueba la adicion de una tarea
        self.task_manager.add_task("Test Task", "This is a test", "2025-03-10", "High")
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.assertEqual(self.task_manager.tasks[0]["titulo"], "Test Task")

    def test_invalid_date(self):
        # Prueba la validacion de formato de fecha incorrecto
        with self.assertRaises(ValueError):
            self.task_manager.add_task("Invalid Task", "Wrong date format", "03-10-2025", "Low")

    def test_modify_task(self):
        # Prueba la modificacion de una tarea existente
        self.task_manager.add_task("Old Task", "Old description", "2025-03-10", "Medium")
        self.task_manager.modify_task(0, titulo="Updated Task", descripcion="Updated description", prioridad="High")
        self.assertEqual(self.task_manager.tasks[0]["titulo"], "Updated Task")
        self.assertEqual(self.task_manager.tasks[0]["descripcion"], "Updated description")
        self.assertEqual(self.task_manager.tasks[0]["prioridad"], "High")

    def test_delete_task(self):
        # Prueba la eliminación de una tarea
        self.task_manager.add_task("Task to delete", "To be removed", "2025-03-10", "Low")
        self.assertEqual(len(self.task_manager.tasks), 1)
        self.task_manager.delete_task(0)
        self.assertEqual(len(self.task_manager.tasks), 0)

if __name__ == "__main__":
    unittest.main()
