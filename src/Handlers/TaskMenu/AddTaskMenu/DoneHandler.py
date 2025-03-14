from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler
from TaskManagement.TaskManager import TaskManager
from TaskManagement.Task import Task

class DoneHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "done"  # Сохраняем состояние пользователя

        # Отправляем итоговое сообщение (имитируя TextHandler)

        await TaskManager.add_task(TextHandler.DATA[0],TextHandler.DATA[1])
        sent_message = await query.message.reply_text(f"Задача создана:\n{TaskManager.TASKS[0]}\n{TextHandler.DATA}")

        # Сохраняем ID нового ответа
        TextHandler.USER_MESSAGES[chat_id] = sent_message.message_id

        # Сбрасываем состояние
        del TextHandler.USER_STATE[chat_id]
