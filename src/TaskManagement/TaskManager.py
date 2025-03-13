from TaskManagement import Task
from Enums import Priority, Status

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class TaskManager:
    def __init__(self):
        self.tasks = {}

    async def add_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def edit_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("edit")

    async def show_tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("show")

    async def delete_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("delete")
