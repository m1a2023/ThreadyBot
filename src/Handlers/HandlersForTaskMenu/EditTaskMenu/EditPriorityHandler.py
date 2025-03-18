from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler


class EditPriorityHandler(Handler):
    @staticmethod
    async def handle(update, context):
        print("edit priority")

        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        context.user_data["state"] = "editTaskPriority"  # Сохраняем состояние пользователя

        sent_message = await query.message.reply_text("Укажите новый приоритет задачи (low, medium, high):")
        context.user_data["bot_message_id"] = sent_message.message_id
