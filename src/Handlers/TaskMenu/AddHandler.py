from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from Handlers.TaskMenu.TextHandler import TextHandler

class AddHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        TextHandler.USER_STATE[chat_id] = "add_opt"  # Сохраняем состояние пользователя

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
        sent_message = await query.message.reply_text("Выберите действие:", reply_markup=reply_markup)

        # Сохраняем ID сообщения, чтобы потом удалить
        TextHandler.USER_MESSAGES[chat_id] = sent_message.message_id
