from telegram import Update
from telegram.ext import ContextTypes

from Handlers.Handler import Handler
from Handlers.TaskMenu.TextHandler import TextHandler
from TaskManagement.TaskManager import TaskManager

class DoneHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "done"  # Фиксируем состояние

        if TextHandler.name == None or TextHandler.description == None:
            await query.message.reply_text("❌ Недостаточно данных для создания задачи. Введите хотя бы имя и описание.")
            return

        task = await TaskManager.add_task(
            TextHandler.name,
            TextHandler.description,
            TextHandler.deadline,
            TextHandler.priority,
            TextHandler.status)

        await query.message.reply_text(f"Задача создана:\n{task}")

        TextHandler.data_clear()
        del TextHandler.USER_STATE[chat_id]
