show_plan
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import json


from Handlers.Handler import Handler
from Handlers.RequestsHandler import show_plan

class ShowProjectPlanHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    proj_id = context.user_data["chosenProject"]

    MAX_MESSAGE_LENGTH = 4096
    plan = show_plan(proj_id)


    if isinstance(plan, dict):
        plan = json.dumps(plan, indent=2, ensure_ascii=False)

    message_length = len(plan)

    if message_length > MAX_MESSAGE_LENGTH:
        parts_count = -(-message_length // MAX_MESSAGE_LENGTH)

        for i in range(parts_count):
            start = i * MAX_MESSAGE_LENGTH
            end = (i + 1) * MAX_MESSAGE_LENGTH
            part = plan[start:end]

            await update.effective_message.reply_markdown(part,reply_markup=reply_markup)
    else:
        await update.effective_message.reply_markdown(plan,reply_markup=reply_markup)

    keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(plan, reply_markup=reply_markup)
