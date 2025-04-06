from datetime import datetime

class Task:
    def __init__(self, titulo, descripcion, due_date, prioridad):
        self.titulo = titulo
        self.descripcion = descripcion
        self.due_date = due_date
        self.prioridad = prioridad

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "due_date": self.due_date,
            "prioridad": self.prioridad
        }
