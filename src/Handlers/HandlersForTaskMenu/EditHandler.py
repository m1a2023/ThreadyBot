from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

class EditHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        context.user_data["taskInfoForEditTask"] = ["Вы отредактировали: "]

        chat_id = query.message.chat_id
        context.user_data["state"] = "editTask"  # Сохраняем состояние пользователя

        sent_message=await query.message.reply_text("Введите имя задачи, которую хотите отредактировать:")
        context.user_data["bot_message_id"] = sent_message.message_id
