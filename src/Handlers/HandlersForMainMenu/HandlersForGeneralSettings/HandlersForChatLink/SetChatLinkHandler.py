from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler


class SetChatLinkHandler(Handler):
    @staticmethod
    async def handle(update, context):

      query = update.callback_query
      await query.answer()

      context.user_data["state"] = "setChatLink"  # Сохраняем состояние пользователя

      sent_message = await query.message.reply_text("Введите новую ссылку:")
      context.user_data["bot_message_id"] = sent_message.message_id
