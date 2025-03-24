from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getTaskById
class ConfirmationDeleteTaskHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Удалить", callback_data="deleteTask")],
            [InlineKeyboardButton("Отмена", callback_data="SettingsOfProjects")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        dataTask = await getTaskById(context.user_data["chosenTask"])
        await query.edit_message_text(f"{dataTask.__str__()}\n\nВы уверены, что хотите удалить задачу?", reply_markup=reply_markup)
