from models.task_manager import TaskManager

class TaskController:
    def __init__(self, view):
        self.view = view
        self.task_manager = TaskManager()
        self.completed = set()

    def get_tasks(self):
        return self.task_manager.tasks

    def add_task(self, titulo, desc, date, priority):
        self.task_manager.add_task(titulo, desc, date, priority)
        self.view.update_task_list()

    def modify_task(self, index, titulo, desc, date, priority):
        self.task_manager.modify_task(index, titulo, desc, date, priority)
        self.view.update_task_list()

    def delete_task(self, index):
        self.task_manager.delete_task(index)
        self.view.update_task_list()

    def mark_as_done(self, index):
        self.completed.add(index)
        self.view.update_task_list()

    def get_completed(self):
        return self.completed