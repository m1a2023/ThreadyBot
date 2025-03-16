from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler
from TaskManagement.TaskManager import TaskManager

class ShowHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

        print("from showhandlerr")
        query = update.callback_query
        await query.answer()

        await TaskManager.show_tasks(update, context)
