from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager

class DeleteHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        context.user_data["taskInfoForDeleteTask"] = ["Вы удалили задачу: "]

        chat_id = query.message.chat_id
        context.user_data["state"] = "deleteTask"  # Устанавливаем состояние

        await query.message.reply_text("Введите имя задачи, которую хотите удалить:")
