from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.TaskMenu.TextHandler import TextHandler

class EditHandler:

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "edit_opt"  # Сохраняем состояние пользователя

        sent_message = await query.message.reply_text("Вы выбрали edit. Введите текст:")

        TextHandler.USER_MESSAGES[chat_id] = sent_message.message_id
