from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from Handlers.TaskMenu.AddHandler import AddHandler
from Handlers.TaskMenu.EditHandler import EditHandler
from Handlers.TaskMenu.DeleteHandler import DeleteHandler

class MenuHandler:
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        await query.answer()

        if query.data == "add":
            return await AddHandler.handle(update, context)
        elif query.data == "edit":
            return await EditHandler.handle(update, context)
        elif query.data == "del":
            return await DeleteHandler.handle(update, context)
