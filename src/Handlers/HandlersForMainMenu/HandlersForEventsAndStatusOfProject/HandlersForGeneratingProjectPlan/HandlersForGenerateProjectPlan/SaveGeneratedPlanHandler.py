from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

class SaveGeneratedPlanHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        await query.answer()

        # где-то здесь сохраняем план

        if "chosenProject" in context.user_data:
            del context.user_data["chosenProject"]

        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("✅ План сохранен", reply_markup=reply_markup)
            
