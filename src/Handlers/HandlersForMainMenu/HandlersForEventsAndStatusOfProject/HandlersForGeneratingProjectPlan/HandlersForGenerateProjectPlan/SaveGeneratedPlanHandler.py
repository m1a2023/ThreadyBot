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
        iam_token = "t1.9euelZrNz8iQycaSm86PmpvGicnIzO3rnpWanoyPkpnJzs2TmcmUz8fGncvl8_dRFyxA-e8Tf2tt_t3z9xFGKUD57xN_a23-zef1656VmpnJz5POxpaLyMiZyMiYk53L7_zF656VmpnJz5POxpaLyMiZyMiYk53L._XvvSoGbd9ue_9bwBRXZESvAeUE0P445j1s_khiDZqwL9hxTI46OfmEMONt2rOiUYKq5mY6KlNyCz4q_5RMVBA"
        folder_id = "b1gc80aslek1slbmcvj9"

        await save_tasks_fom_plan(proj_id,iam_token,folder_id)

        if "chosenProject" in context.user_data:
            del context.user_data["chosenProject"]

        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("✅ План сохранен", reply_markup=reply_markup)
