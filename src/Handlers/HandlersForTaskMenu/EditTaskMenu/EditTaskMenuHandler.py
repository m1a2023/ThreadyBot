from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

class EditTaskMenuHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        task_name = context.user_data["task_name"]
        if context.user_data["task_manager"].found_task(task_name,update,context):

            keyboard = [
                [InlineKeyboardButton("Изменить имя", callback_data="editTaskName")],
                [InlineKeyboardButton("Изменить описание", callback_data="editTaskDescription")],
                [InlineKeyboardButton("Изменить дедлайн", callback_data="editTaskDeadline")],
                [InlineKeyboardButton("Изменить приоритет", callback_data="editTaskPriority")],
                [InlineKeyboardButton("Изменить статус", callback_data="editTaskStatus")],
                [
                    InlineKeyboardButton("Отмена", callback_data="edit_cancel"),
                    InlineKeyboardButton("Готово", callback_data="edit_done")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            #вот тут надо адаптировать под метод process message
            sent_message=await update.message.reply_text(f"Вы выбрали для редактирования задачу: {task_name}\nВыберите действие:",reply_markup=reply_markup)
        else:
            sent_message=await update.message.reply_text("Такой задачи нет")
        context.user_data["bot_message_id"] = sent_message.message_id
