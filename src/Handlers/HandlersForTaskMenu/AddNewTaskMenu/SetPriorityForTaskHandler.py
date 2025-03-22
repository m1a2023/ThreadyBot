from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler


class SetPriorityForTaskHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        context.user_data["state"] = "setPriorityForTask"  # Сохраняем состояние пользователя

        keyboard = [
            [InlineKeyboardButton("Низкий", callback_data="priorityTaskLow")],
            [InlineKeyboardButton("Средний", callback_data="priorityTaskMedium")],
            [InlineKeyboardButton("Высокий", callback_data="priorityTaskHigh")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        sent_message = await query.message.reply_text("Выберите приоритет задачи:", reply_markup = reply_markup)
        context.user_data["bot_message_id"] = sent_message.message_id
