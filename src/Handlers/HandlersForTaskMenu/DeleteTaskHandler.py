from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from Handlers.RequestsHandler import deleteTaskById

class DeleteTaskHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        task_id = context.user_data["chosenTask"]
        await deleteTaskById(task_id)

        return await SettingsOfProjectsHandler.handle(update, context)
