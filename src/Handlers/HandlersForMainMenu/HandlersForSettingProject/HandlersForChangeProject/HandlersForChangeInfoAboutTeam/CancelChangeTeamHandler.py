from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.ChangeProjectHandler import ChangeProjectHandler

class CancelChangeTeamHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Очищаем ненужные данные из контекста
    keys_to_remove = [
      "state",
      "team",
      "bot_message_id"
    ]
    for key in keys_to_remove:
      if key in context.user_data:
        del context.user_data[key]

    return await ChangeProjectHandler.handle(update, context)
