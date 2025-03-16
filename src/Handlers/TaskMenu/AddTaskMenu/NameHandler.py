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
        TextHandler.USER_STATE[chat_id] = "add_name"  # Сохраняем состояние пользователя

        await query.message.reply_text("Введите имя задачи:")
