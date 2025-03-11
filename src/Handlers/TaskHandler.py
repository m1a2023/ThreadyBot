from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager

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
