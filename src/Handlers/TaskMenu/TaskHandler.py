from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager
from Models.bot_app import BotApp

from Handlers.Handler import Handler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

class TaskHandler(Handler):
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

        await query.edit_message_text("Привет! Выберите действие:", reply_markup=reply_markup)
