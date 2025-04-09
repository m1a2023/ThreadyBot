from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import save_tasks_fom_plan

class SaveGeneratedPlanHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        await query.answer()

        proj_id = context.user_data["chosenProject"]
        iam_token = "t1.9euelZqdkZvMj8iWm5mXno2TmJCJju3rnpWanoyPkpnJzs2TmcmUz8fGncvl8_d4PylA-e8kS348_d3z9zhuJkD57yRLfjz9zef1656Vmoyek8zNlZiQjI3Jy4_HlpKR7_zF656Vmoyek8zNlZiQjI3Jy4_HlpKR.qkn44r7OuaM8AL3sNH7hXdjuUk00yaRG4EQoMzlW-hBg-z7El6OTiLYr7vyRWN_6JoehuRBtMZq4TVeG9NiWAg"
        folder_id = "b1gc80aslek1slbmcvj9"

        await save_tasks_fom_plan(proj_id,iam_token,folder_id)

        if "chosenProject" in context.user_data:
            del context.user_data["chosenProject"]

        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("✅ План сохранен", reply_markup=reply_markup)
