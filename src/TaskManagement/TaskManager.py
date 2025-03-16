from TaskManagement.Task import Task
from Enums import Priority, Status

from telegram import Update
from telegram.ext import ContextTypes

class TaskManager:
    TASKS = []  # Храним список задач

    @staticmethod
    async def add_task(name, description, deadline=None, priority=None, status=None):
        print("add task from manager")
        task = Task(name, description, deadline, priority, status)
        TaskManager.TASKS.append(task)
        return task

    @staticmethod
    async def get_tasks():
        print("from get tasks")
        if not TaskManager.TASKS:
            return "Список задач пуст."

        return "\n\n".join([f"{i + 1}. {task}" for i, task in enumerate(TaskManager.TASKS)])

    @staticmethod
    async def show_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("from show tasks")
        tasks_text = await TaskManager.get_tasks()

        if update.message:
            await update.message.reply_text(tasks_text)
        elif update.callback_query:
            await update.callback_query.message.reply_text(tasks_text)

    @staticmethod
    async def delete_task(task_name,update, context) -> any:
        task_to_delete = next((task for task in TaskManager.TASKS if task._name == task_name), None)

        if task_to_delete:
            TaskManager.TASKS.remove(task_to_delete)
            response_text = f"Задача '{task_name}' удалена."
        else:
            response_text = f"Задача '{task_name}' не найдена."

        return response_text

    @staticmethod
    async def edit_task(update, context):
        await update.message.reply_text("✏ Редактирование задач пока не реализовано.")
