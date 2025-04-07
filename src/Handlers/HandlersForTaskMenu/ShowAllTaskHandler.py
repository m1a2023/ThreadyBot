from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.RequestsHandler import getAllTasks
from TaskManagement.TaskManager import TaskManager

class ShowAllTaskHandler(Handler):
    # Форматирует задачи в красивый вывод
    @staticmethod
    def format_task(task):
        deadline = task.get("deadline")
        if deadline:
            deadline = datetime.fromisoformat(deadline).strftime("%d.%m.%Y")
        else:
            deadline = "Нет дедлайна"

        # Форматируем задачу
        formatted_task = (
            f"Задача: {task['title']}\n"
            f"Описание: {task['description']}\n"
            f"Статус: {task['status']}\n"
            f"Приоритет: {task['priority']}\n"
            f"Дедлайн: {deadline}\n"
        )
        return formatted_task
    
    @staticmethod
    def format_tasks_by_status(tasks):
        # Группируем задачи по статусу
        tasks_by_status = {}
        for task in tasks:
            status = task["status"]
            if status not in tasks_by_status:
                tasks_by_status[status] = []
            tasks_by_status[status].append(task)

        # Форматируем задачи для каждой группы
        formatted_list_task = []
        for status, tasks_in_status in tasks_by_status.items():
            formatted_tasks = [ShowAllTaskHandler.format_task(task) for task in tasks_in_status]
            formatted_list_task.append(f"~~~ {status.upper()} ~~~\n" + "\n".join(formatted_tasks))
        
        return formatted_list_task

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        await TaskManager.get_and_update_list_tasks(update, context, context.user_data["chosenProject"])
        tasks = await getAllTasks(context.user_data["chosenProject"])
        formatted_list_task = "\n".join(ShowAllTaskHandler.format_tasks_by_status(tasks))

        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="SettingsOfProjects")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(f"Все задачи:\n{formatted_list_task}", reply_markup=reply_markup)

        
        
