from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager

from Handlers.Handler import Handler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

class MainTaskMenuHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Добавить задачу", callback_data="add")],
            [InlineKeyboardButton("Редактировать задачу", callback_data="edit")],
            [InlineKeyboardButton("Удалить задачу", callback_data="del")],
            [InlineKeyboardButton("Показать задачи", callback_data="show")],
            [InlineKeyboardButton("Назад", callback_data="cancelTaskMenu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        sent_message=await query.edit_message_text("Выберите действие:", reply_markup=reply_markup)
        context.user_data["bot_message_id"] = sent_message.message_id
