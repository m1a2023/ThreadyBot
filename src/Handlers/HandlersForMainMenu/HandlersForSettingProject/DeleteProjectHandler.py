from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager

class DeleteProjectHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        context.user_data["projectInfoForDeleteProject"] = ["Вы удалили проект: "]

        chat_id = query.message.chat_id
        context.user_data["state"] = "deleteProject"  # Устанавливаем состояние

        await query.message.reply_text("Введите имя проекта, который хотите удалить:")
