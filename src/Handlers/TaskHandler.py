from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager
from Enums.Priority import Priority
from Enums.Status import Status

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters,CallbackContext, ConversationHandler

from typing import Any

task_manager = TaskManager()
NAME, DESCRIPTION, DEADLINE, PRIORITY, STATUS = range(5)

class TaskHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        await update.message.reply_text("Choose /add_task, /edit_task, /delete_task or /get_task")

        """
        БЛОК ДОБАВДЕНИЯ ЗАДАЧИ
        """

    async def add_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("First, please enter the task name:")
        return NAME

    def get_task_name(self, update: Update, context: CallbackContext):
        global task_name
        task_name = update.message.text
        update.message.reply_text("Now, please enter the deadline:")
        return DEADLINE

    async def get_task_description(self, update: Update, context: CallbackContext):
        global task_description
        task_description = update.message.text
        await update.message.reply_text("Now, please enter the deadline (YYYY-MM-DD):")
        return DEADLINE

    async def get_task_deadline(self, update: Update, context: CallbackContext):
        global task_deadline
        task_deadline = update.message.text
        await update.message.reply_text("Now, please enter the priority (Low, Medium, High):")
        return PRIORITY

    async def get_task_priority(self, update: Update, context: CallbackContext):
        global task_priority

        if update.message.text == "Low":
            task_priority = Priority.LOW
        elif update.message.text == "Mediun":
            task_priority = Priority.MEDIUM
        elif update.message.text == "High":
            task_priority = Priority.HIGH
        else:
            await update.message.reply_text("Please, enter correct priority")
            return PRIORITY

        await update.message.reply_text("Now, please enter the status (ToDo, InProgress, Done):")
        return STATUS

    async def get_task_status(self, update: Update, context: CallbackContext):
        global task_status

        if update.message.text == "ToDO":
            task_status = Status.TODO
        elif update.message.text == "InProgress":
            task_status = Status.IN_PROGRESS
        elif update.message.text == "Done":
            task_status = Status.DONE
        else:
            await update.message.reply_text("Please, enter correct status")
            return STATUS

        task_manager.add_task(
            task_name,
            task_description,
            task_deadline,
            task_priority,
            task_status
        )

        return ConversationHandler.END

    async def cancel(self, update: Update, context: CallbackContext):
        await update.message.reply_text("Task creation cancelled")
        return ConversationHandler.END

    #надо будет как-то добавить ConversationHandler в main.py чтобы методы вызывались по порядку, но я хз как

    """
    БЛОК РЕДАКТИРОВАНИЯ ЗАДАЧИ
    """


    async def edit_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Please, enter id of the task that you wont to edit")
