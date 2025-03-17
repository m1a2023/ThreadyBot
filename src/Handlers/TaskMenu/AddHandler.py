from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler
from TaskManagement.Task import Task

class AddHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        context.user_data["task"] = Task()

        keyboard = [
            [InlineKeyboardButton("Добавить имя", callback_data="name")],
            [InlineKeyboardButton("Добавить описание", callback_data="description")],
            [InlineKeyboardButton("Назначить дедлайн", callback_data="deadline")],
            [InlineKeyboardButton("Назначить приоритет", callback_data="priority")],
            [InlineKeyboardButton("Назначить статус", callback_data="status")],
            [
                InlineKeyboardButton("Отмена", callback_data="cancel"),
                InlineKeyboardButton("Готово", callback_data="done")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопками
        await query.message.reply_text("Выберите действие:", reply_markup=reply_markup)
