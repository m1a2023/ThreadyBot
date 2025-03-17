from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler

class EditStatusHandler(Handler):
    @staticmethod
    async def handle(update, context):
        print("edit status")

        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        context.user_data["state"] = "editTaskStatus"  # Сохраняем состояние пользователя

        sent_message = await query.message.reply_text("Укажите новый приоритет задачи (todo, in progress, done):")
        context.user_data["bot_message_id"] = sent_message.message_id
