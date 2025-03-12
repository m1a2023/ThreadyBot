from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager
from Models.bot_app import BotApp
from TaskManagement.TaskConversation import TaskConversation

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

class TaskHandler(Handler):

    @classmethod
    def init(cls):
        app = BotApp().get_application()
        task_manager = BotApp().get_task_manager()
        cls.register_handlers(app, task_manager)

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

    @classmethod
    def register_handlers(cls, app: Application, task_manager: TaskManager):
        app.add_handler(CommandHandler("show_tasks", task_manager.show_tasks))
        app.add_handler(CommandHandler("add_task", task_manager.add_task))
        app.add_handler(TaskConversation.get_conversation_handler())

        app.add_handler(CommandHandler("edit_task", task_manager.edit_task))
        app.add_handler(CommandHandler("delete_task", task_manager.delete_task))
