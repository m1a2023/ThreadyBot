from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from telegram.error import BadRequest

from Handlers.Handler import Handler

from Handlers.TaskMenu.AddTaskMenu.NameHandler import NameHandler
from Handlers.TaskMenu.AddTaskMenu.DescriptionHandler import DescriptionHandler
from Handlers.TaskMenu.TaskHandler import TaskHandler

class EditDoneHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.user_data["task_manager"].edit_task(update, context)
    # Получаем chat_id
    if update.message:
      chat_id = update.message.chat_id
    else:
      chat_id = update.callback_query.message.chat_id

    last_bot_message_id = context.user_data.get("IdLastMessageFromBot")

    # Удаляем последнее сообщение бота (если есть)
    if last_bot_message_id:
      try:
        await context.bot.delete_message(chat_id, last_bot_message_id)
      except BadRequest as e:
        print(f"Ошибка при удалении последнего сообщения бота: {e}")

    # Очищаем все данные, связанные с редактированием задачи
    keys_to_remove = [
      "state",
      "task",
      "taskInfoForCreateTask",
      "IdLastMessageFromBot",
      "bot_message_id"
    ]
    for key in keys_to_remove:
      if key in context.user_data:
        del context.user_data[key]

    return await TaskHandler.handle(update, context)
