from datetime import datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForCurrentTask.CreateKeyboardForCurrentTasks import CreateKeyboardForCurrentTasks
from Handlers.RequestsHandler import getTaskById, getUserNameById

class ShowInfoAndFastEditTasksHandler(Handler): 
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    await query.answer()
    task_id = context.user_data["taskInCurrentTasks"]
    task = await getTaskById(task_id)
    if task.developer is not None:
      developer_link = f'<a href="tg://user?id={task.developer}">{await getUserNameById(task.developer)}</a>'
    text_about_task = (f"Задача: {task.title}\n"
                f"Описание: {task.description}\n"
                f"Дедлайн: {datetime.fromisoformat(task.deadline).strftime('%d.%m.%Y')}\n"
                f"Приоритет: {task.priority}\n"
                f"Статус: {task.status}\n"
                f"Исполнитель: { developer_link if task.developer else 'Не указан'}")

    keyboard = []
    if task.status == "in_progress":
      keyboard.append([InlineKeyboardButton("✅ Выполнено", callback_data="FastEditTaskForStatusDone")])
    else:
      keyboard.append([InlineKeyboardButton("🔄 Начать работу", callback_data="FastEditTaskForStatusInProgress")])
    if task.developer is None:
      keyboard.append([InlineKeyboardButton("🧑‍💻 Назначить исполнителя", callback_data="FastEditTaskForChangeDeveloper")])
    
    keyboard.append([InlineKeyboardButton("📅 Изменить дедлайн", callback_data="FastEditTaskForChangeDeadline")])
    keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text_about_task, reply_markup=reply_markup, parse_mode="HTML")