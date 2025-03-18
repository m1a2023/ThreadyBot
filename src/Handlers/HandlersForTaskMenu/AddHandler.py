from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from TaskManagement.Task import Task

class AddHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        if "task" not in context.user_data:
            """ Эта штука будет сохранять в контексте инфу о проекте при создании для сохранения в бд """
            context.user_data["task"] = Task()
            """ Эти штуки нужны для красивого вывода (комментариев для пользователя) при создании проекта """
            context.user_data["taskInfoForCreateTask"] = ["Вы ввели:"]


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
        context.user_data["bot_message_id"] = sent_message.message_id
