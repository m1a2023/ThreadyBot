from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.TaskMenu.TextHandler import TextHandler
from TaskManagement.TaskManager import TaskManager

class DeleteHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "delete_opt"  # Устанавливаем состояние

        await query.message.reply_text("Введите имя задачи, которую хотите удалить:")
