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
        context.user_data["state"] = "setPriorityForTask"  # Сохраняем состояние пользователя

        sent_message = await query.message.reply_text("Выберите приоритет задачи: low, medium, high")
        context.user_data["bot_message_id"] = sent_message.message_id
