from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from telegram.error import BadRequest

from Handlers.Handler import Handler

from Handlers.HandlersForTaskMenu.MainTaskMenuHandler import MainTaskMenuHandler
from Handlers.RequestsHandler import updateTaskById

class SaveEditTaskHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

    changed_task = context.user_data["changedTask"].to_dict()
    new_info = {}
    for key in changed_task:
      if changed_task[key] != "":
        # Если значение — это объект datetime, преобразуем его в строку
        if isinstance(changed_task[key], datetime):
          new_info[key] = changed_task[key].isoformat()
        else:
          new_info[key] = changed_task[key]
    await updateTaskById(int(context.user_data["chosenTask"]), new_info)

    # Очищаем все данные, связанные с редактированием задачи
    keys_to_remove = [
      "state",
      "task",
      "taskInfoForEditTask",
      "IdLastMessageFromBot",
      "bot_message_id"
    ]
    for key in keys_to_remove:
      if key in context.user_data:
        del context.user_data[key]

    return await MainTaskMenuHandler.handle(update, context)
