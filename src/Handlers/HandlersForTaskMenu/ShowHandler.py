from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from TaskManagement.TaskManager import TaskManager

class ShowHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

        print("from showhandlerr")
        query = update.callback_query
        await query.answer()

        task_manager = context.user_data["task_managers"].get(context.user_data["project_name"])
        await task_manager.show_tasks(update, context)
