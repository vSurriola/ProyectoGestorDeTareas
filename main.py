if __name__ == "__main__":
    import tkinter as tk
    from views.task_view import TaskView

    root = tk.Tk()
    app = TaskView(root)
    root.mainloop()
