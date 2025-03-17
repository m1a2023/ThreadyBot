from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from telegram.error import BadRequest

from Handlers.Handler import Handler

class CancelCreateProjectHandler(Handler): 
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем chat_id
    if update.message:
      chat_id = update.message.chat_id  
    else: 
      chat_id = update.callback_query.message.chat_id

    # Удаляем последнее сообщение бота (если есть)
    last_bot_message_id = context.user_data.get("IdLastMessageFromBot")
    if last_bot_message_id:
      try:
        await context.bot.delete_message(chat_id, last_bot_message_id)
      except BadRequest as e:
        print(f"Ошибка при удалении последнего сообщения бота: {e}")

    # Очищаем все данные, связанные с созданием проекта
    keys_to_remove = [
      "state",
      "project",
      "projectInfoForCreateProject",
      "IdLastMessageFromBot",
      "bot_message_id"
    ]
    for key in keys_to_remove:
      if key in context.user_data:
        del context.user_data[key]

    return await SettingsOfProjectsHandler.handle(update, context)
