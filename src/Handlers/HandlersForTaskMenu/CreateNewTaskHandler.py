from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

from TaskManagement.Task import Task

class CreateNewTaskHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        if "task" not in context.user_data:
            context.user_data["task"] = Task()
            context.user_data["taskInfoForCreateTask"] = ["Вы ввели:"]

        keyboard = [
            [InlineKeyboardButton("Добавить имя", callback_data="setNameForCreateTask")],
            [InlineKeyboardButton("Добавить описание", callback_data="setDescriptionForCreateTask")],
            [InlineKeyboardButton("Назначить дедлайн", callback_data="setDeadlineForCreateTask")],
            [InlineKeyboardButton("Назначить приоритет", callback_data="setPriorityForCreateTask")],
            [InlineKeyboardButton("Назначить статус", callback_data="setStatusForCreateTask")],
            [
                InlineKeyboardButton("Отмена", callback_data="cancelCreateTask"),
                InlineKeyboardButton("Сохранить", callback_data="saveNewTaskForCreateTask")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопками
        await query.edit_message_text("Выберите действие:", reply_markup=reply_markup)
