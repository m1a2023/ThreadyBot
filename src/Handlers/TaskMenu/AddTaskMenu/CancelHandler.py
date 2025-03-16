from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler
from TaskManagement.TaskManager import TaskManager
from TaskManagement.Task import Task

class CancelHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "cancel"  # Сохраняем состояние пользователя
        TextHandler.data_clear()

        await query.message.reply_text(f"Добавление задачи прервано\n{TextHandler.USER_STATE}")

        # Сбрасываем состояние
        del TextHandler.USER_STATE[chat_id]
