from TaskManagement.TaskManager import TaskManager
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

task_manager = TaskManager()

@staticmethod
def registration_task_commands(application):
    application.add_handler(CommandHandler("add_task", task_manager.add_task))
