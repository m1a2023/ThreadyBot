from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler

class PriorityHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "add_priority"  # Сохраняем состояние пользователя

        await query.message.reply_text("Выберите приоритет задачи: low, medium, high")
