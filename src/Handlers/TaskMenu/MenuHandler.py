from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from Handlers.TaskMenu.AddHandler import AddHandler
from Handlers.TaskMenu.EditHandler import EditHandler
from Handlers.TaskMenu.DeleteHandler import DeleteHandler

from Handlers.TaskMenu.AddTaskMenu.NameHandler import NameHandler
from Handlers.TaskMenu.AddTaskMenu.DescriptionHandler import DescriptionHandler
from Handlers.TaskMenu.AddTaskMenu.DeadlineHandler import DeadlineHandler
from Handlers.TaskMenu.AddTaskMenu.PriorityHandler import PriorityHandler
from Handlers.TaskMenu.AddTaskMenu.StatusHandler import StatusHandler

class MenuHandler:
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        print("aboba")

        query = update.callback_query
        await query.answer()

        if query.data == "add":
            return await AddHandler.handle(update, context)
        elif query.data == "edit":
            return await EditHandler.handle(update, context)
        elif query.data == "del":
            return await DeleteHandler.handle(update, context)
        elif query.data == "name":
            return await NameHandler.handle(update, context)
        elif query.data == "description":
            return await DescriptionHandler.handle(update, context)
        elif query.data == "deadline":
            return await DeadlineHandler.handle(update, context)
        elif query.data == "priority":
            return await PriorityHandler.handle(update, context)
        elif query.data == "status":
            return await StatusHandler.handle(update, context)
