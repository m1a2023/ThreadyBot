from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager
from Models.ThreadyBot import ThreadyBot

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

task_manager = TaskManager()
NAME, DESCRIPTION, DEADLINE, PRIORITY, STATUS = range(5)

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
