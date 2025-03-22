from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager


class ChooseTaskHandler(Handler):
  @staticmethod
  async def handle(update, context):

    query = update.callback_query
    await query.answer()

    await TaskManager.get_and_update_list_tasks(update, context, context.user_data["chosenProject"])

    if context.user_data["task_manager"].tasks == []:
      keyboard = [
        [InlineKeyboardButton(f"Создать задачу", callback_data="createNewTask")],
        [InlineKeyboardButton("Назад", callback_data="SettingsOfProjects")]
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text(text="Нет задач по выбранному проекту", reply_markup=reply_markup)
      context.user_data["state"] = None

    else:
        keyboard = []
        # Собираем кнопки с задачами
        tasks = await context.user_data["task_manager"].get_tasks_names_and_id()
        for task in tasks:
          keyboard.append([InlineKeyboardButton(f"{task[0]}", callback_data=f"chosenTask_{task[1]}")])
        keyboard.append([InlineKeyboardButton("Назад", callback_data="SettingsOfProjects")])

        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Выберите задачу: ", reply_markup=reply_markup)
