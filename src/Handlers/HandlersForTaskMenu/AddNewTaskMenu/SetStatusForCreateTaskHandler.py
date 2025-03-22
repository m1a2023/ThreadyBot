from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler


class SetStatusForCreateTaskHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        context.user_data["state"] = "setStatusForTask"  # Сохраняем состояние пользователя

        keyboard = [
            [InlineKeyboardButton("TODO", callback_data="statusTaskTodo")],
            [InlineKeyboardButton("В процессе", callback_data="statusTaskInProgress")],
            [InlineKeyboardButton("Выполнено", callback_data="statusTaskDone")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)


        sent_message = await query.message.reply_text("Выберите статус задачи:", reply_markup = reply_markup)
        context.user_data["bot_message_id"] = sent_message.message_id
