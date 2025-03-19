from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class DeleteDeveloperHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    # Получаем chat_id
    chat_id = query.message.chat_id

    # Устанавливаем состояние "deleteDeveloper" в context.user_data, 
    # это нужно, чтобы обработать конкретный момент (например, добавление названия) в TextHandler
    context.user_data["state"] = "deleteDeveloper"

    # По-хорошему, здесь должен быть не id 
    sent_message = await query.message.reply_text("Введите id разработчика для удаления:")

    # Сохраняем ID сообщения бота в context.user_data
    # Нужно, чтобы потом удалить сообщение бота для красивого вывода 
    context.user_data["bot_message_id"] = sent_message.message_id
