from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler


class ShowCurrentPlanHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        
        query = update.callback_query
        await query.answer()

        planText = context.user_data["current_plan"]

        if planText is None:
            keyboard = [
                [InlineKeyboardButton("🆕 Сгенерировать план", callback_data="generateNewPlan")],
                [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"⚠️ У вас нет плана. Хотите сгенерировать?", reply_markup=reply_markup)
        else:
            keyboard = [
                [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(f"{planText}", reply_markup=reply_markup)