from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler

class NameHandler(Handler):
    @staticmethod
    async def handle(update, context):
        print("name add")

        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        context.user_data["state"] = "setNameForTask"  # Сохраняем состояние пользователя

        sent_message = await query.message.reply_text("Введите имя задачи:")
        context.user_data["bot_message_id"] = sent_message.message_id
