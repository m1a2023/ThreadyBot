from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager
from Models.bot_app import BotApp

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

class TaskHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        if update.message:
            await update.message.reply_html(
                "Choose your action: " + \
                "\n/show_tasks" + \
                "\n/add_task" + \
                "\n/edit_task" + \
                "\n/delete_task",
                reply_markup=ForceReply(selective=True)
            )
        app = BotApp().get_application()

        app.add_handler(CommandHandler("show_tasks", TaskManager.show_tasks))
        app.add_handler(CommandHandler("add_task", TaskManager.add_task))
        app.add_handler(CommandHandler("edit_task", TaskManager.edit_task))
        app.add_handler(CommandHandler("delete_task", TaskManager.delete_task))
