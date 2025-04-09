from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any
import json

from Handlers.Handler import Handler
from Handlers.RequestsHandler import show_plan

class ShowCurrentPlanHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

        query = update.callback_query
        await query.answer()

        proj_id = context.user_data["chosenProject"]
        planText = await show_plan(proj_id)
        MAX_MESSAGE_LENGTH = 4096

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

            message_length = len(planText)

            if message_length > MAX_MESSAGE_LENGTH:
                parts_count = -(-message_length // MAX_MESSAGE_LENGTH)

                for i in range(parts_count):
                    start = i * MAX_MESSAGE_LENGTH
                    end = (i + 1) * MAX_MESSAGE_LENGTH
                    part = planText[start:end]

                    await update.effective_message.reply_markdown(part,reply_markup=reply_markup)
            else:
                await update.effective_message.reply_markdown(planText,reply_markup=reply_markup)
