from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler


class EditProjectNameHandler(Handler):
    @staticmethod
    async def handle(update, context):

        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        context.user_data["state"] = "editProjectName"  # Сохраняем состояние пользователя

        sent_message = await query.message.reply_text("Введите новое имя проекта:")
        context.user_data["bot_message_id"] = sent_message.message_id
