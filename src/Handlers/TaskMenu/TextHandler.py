from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

class TextHandler(Handler):
    USER_STATE = {}  # Сохраняем выбранную опцию
    USER_MESSAGES = {}  # Запоминаем ID сообщений пользователя и бота
    DATA = []

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        chat_id = update.message.chat_id
        user_text = update.message.text
        user_message_id = update.message.message_id

        if chat_id in TextHandler.USER_STATE:
            selected_option = TextHandler.USER_STATE[chat_id]  # Какая опция выбрана

            if chat_id in TextHandler.USER_MESSAGES:
                try:
                    await context.bot.delete_message(chat_id, TextHandler.USER_MESSAGES[chat_id])
                    await context.bot.delete_message(chat_id, user_message_id)
                except Exception:
                    pass


            #TextHandler.DATA.append(user_text)
            # Формируем ответ в зависимости от выбранной опции
            sent_message = await update.message.reply_text(f"Вы написали в {selected_option.capitalize()}: {user_text}")

            # Сохраняем ID нового ответа
            TextHandler.USER_MESSAGES[chat_id] = sent_message.message_id

            # Сбрасываем состояние пользователя
            del TextHandler.USER_STATE[chat_id]
