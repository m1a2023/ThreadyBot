from telegram import Update
from telegram.ext import ContextTypes

from Handlers.Handler import Handler
from Handlers.TaskMenu.TextHandler import TextHandler
from TaskManagement.TaskManager import TaskManager

class EditDoneHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "edit_done"  # Фиксируем состояние

        task = await TaskManager.edit_task(
            update,
            context,
            TextHandler.name,
            TextHandler.description,
            TextHandler.deadline,
            TextHandler.priority,
            TextHandler.status
        )

        await query.message.reply_text(f"Задача изменена:\n{task}")

        TextHandler.data_clear()
        del TextHandler.USER_STATE[chat_id]
