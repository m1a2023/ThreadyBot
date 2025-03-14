from TaskManagement.Task import Task
from Enums import Priority, Status

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


class TaskManager:
    TASKS = []

    @staticmethod
    async def add_task(name, description, deadline=None, priority: Priority=None, status: Status=None):
        task = Task(name, description, deadline, priority, status)
        TaskManager.TASKS.append(task)

    @staticmethod
    async def edit_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("edit")

    @staticmethod
    async def show_tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("show")

    @staticmethod
    async def delete_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("delete")
