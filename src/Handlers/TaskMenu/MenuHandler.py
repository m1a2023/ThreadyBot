from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from Handlers.TaskMenu.AddHandler import AddHandler
from Handlers.TaskMenu.EditHandler import EditHandler
from Handlers.TaskMenu.DeleteHandler import DeleteHandler
from Handlers.TaskMenu.ShowHandler import ShowHandler

from Handlers.TaskMenu.AddTaskMenu.NameHandler import NameHandler
from Handlers.TaskMenu.AddTaskMenu.DescriptionHandler import DescriptionHandler
from Handlers.TaskMenu.AddTaskMenu.DeadlineHandler import DeadlineHandler
from Handlers.TaskMenu.AddTaskMenu.PriorityHandler import PriorityHandler
from Handlers.TaskMenu.AddTaskMenu.StatusHandler import StatusHandler
from Handlers.TaskMenu.AddTaskMenu.DoneHandler import DoneHandler
from Handlers.TaskMenu.AddTaskMenu.CancelHandler import CancelHandler

from Handlers.TaskMenu.EditTaskMenu.EditDoneHandler import EditDoneHandler

class MenuHandler:
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        print("from menuHandler")

        query = update.callback_query
        await query.answer()
        #кнопки главного меню работы с задачами
        if query.data == "add":
            return await AddHandler.handle(update, context)
        elif query.data == "edit":
            return await EditHandler.handle(update, context)
        elif query.data == "del":
            return await DeleteHandler.handle(update, context)
        elif query.data == "show":
            return await ShowHandler.handle(update, context)
        #кнопки меню добавления задачи
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
        elif query.data == "done":
            return await DoneHandler.handle(update,context)
        elif query.data == "cancel":
            return await CancelHandler.handle(update,context)
        #кнопки меню редактирования задачи
        elif query.data == "edit_done":
            return await EditDoneHandler.handle(update,context)
