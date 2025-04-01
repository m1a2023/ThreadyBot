from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getProjectById
class ConfirmationDeleteProjectHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("🗑️ Удалить", callback_data="deleteProject")],
            [InlineKeyboardButton("❌ Отмена", callback_data="SettingsOfProjects")]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        dataProject = await getProjectById(context.user_data["chosenProject"])
        await query.edit_message_text(f"{dataProject.__str__()}\n\nУверены, что хотите удалить проект?", reply_markup=reply_markup, disable_web_page_preview=True)
