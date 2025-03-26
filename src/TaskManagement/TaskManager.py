from telegram import Update
from telegram.ext import ContextTypes

from Handlers.RequestsHandler import getAllTasks

class TaskManager:
    def __init__(self):
        self.tasks = []

    async def get_and_update_list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE, project_id: int):
        if "task_manager" not in context.user_data:
            context.user_data["task_manager"] = TaskManager()
        context.user_data["task_manager"].tasks = await getAllTasks(project_id)

    async def get_tasks_names_and_id(self):
        list_of_task = []
        if not self.tasks:
           return []
        for task in self.tasks:
            list_of_task.append((task["title"], task["id"]))
        return list_of_task
    
    async def get_projects_names(self): # Вернет список с именами проектов
        list_of_task = []
        if not self.tasks:
           return []
        for tasks in self.tasks:
            list_of_task.append(tasks["title"])
        return list_of_task