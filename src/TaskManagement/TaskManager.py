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










    # TASKS = []  # Храним список задач

    # async def add_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):

        
    #     TaskManager.TASKS.append(context.user_data["task"])

    # async def get_tasks():
    #     print("from get tasks")
    #     if not TaskManager.TASKS:
    #         return "Список задач пуст."

    #     return "\n\n".join([f"{i + 1}. {task}" for i, task in enumerate(TaskManager.TASKS)])

    # async def show_tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     print("from show tasks")
    #     tasks_text = await TaskManager.get_tasks()

    #     if update.message:
    #         await update.message.reply_text(tasks_text)
    #     elif update.callback_query:
    #         await update.callback_query.message.reply_text(tasks_text)

    # async def delete_task(self, task_name,update: Update, context: ContextTypes.DEFAULT_TYPE) -> any:
    #     task_to_delete = context.user_data["task_manager"].found_task(task_name,update,context)

    #     if task_to_delete:
    #         TaskManager.TASKS.remove(task_to_delete)
    #         response_text = f"Задача '{task_name}' удалена."
    #     else:
    #         response_text = f"Задача '{task_name}' не найдена."

    #     return response_text

    # async def edit_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     #context.user_data["task_manager"].TASKS.remove(context.user_data["task_manager"].found_task(context.user_data["task_name"],update,context))
    #     #TaskManager.TASKS.append()

    #     #тут надо будет сделать функционал, который будет удалять из бд предыдущий вариант задачи и добавлять отредактированый

    #     print("отредачено")

    # def found_task(self,task_name,update: Update, context: ContextTypes.DEFAULT_TYPE):
    #     return next((task for task in context.user_data["task_manager"].TASKS if task._name == task_name), None)
