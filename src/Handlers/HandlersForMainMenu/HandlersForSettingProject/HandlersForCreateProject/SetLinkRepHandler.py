from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class SetLinkRepHandler(Handler): 
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Получаем chat_id
    chat_id = query.message.chat_id

    # Устанавливаем состояние "setLinkForCreateProject" в context.user_data
    context.user_data["state"] = "setLinkForCreateProject"

    # Отправляем сообщение с запросом имени проекта
    sent_message = await query.message.reply_text("Вставте ссылку на репозиторий, если она есть:")

    # Сохраняем ID сообщения бота в context.user_data
    context.user_data["bot_message_id"] = sent_message.message_id

