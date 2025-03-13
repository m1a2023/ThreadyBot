from telegram import Update
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

        sent_message = await query.message.reply_text("Выберите приоритет задачи:") #потом надо будет к этому сообщению кнопки с приоритетом приделать

        TextHandler.USER_MESSAGES[chat_id] = sent_message.message_id
