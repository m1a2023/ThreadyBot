from TaskManagement import Task
from Enums import Priority, Status

class TaskManager:
    def __init__(self):
        self.tasks = {}

    def add_task(self, name, description, deadline, priority: Priority, status: Status):
        task = Task(name, description, deadline, priority, status)
        self.tasks[task.task_id] = task
        return task.task_id

    def edit_task(self, task_id, **kwargs):
        if task_id in self.tasks:
            self.tasks[task_id].edit_task(**kwargs)
            return True
        return False

    def delete_task(self, task_id):
        return self.tasks.pop(task_id, None) is not None
