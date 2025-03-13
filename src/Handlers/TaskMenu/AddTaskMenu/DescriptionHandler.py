from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler

class DescriptionHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "add_description"  # Сохраняем состояние пользователя

        sent_message = await query.message.reply_text("Введите описание задачи:")

        TextHandler.USER_MESSAGES[chat_id] = sent_message.message_id
