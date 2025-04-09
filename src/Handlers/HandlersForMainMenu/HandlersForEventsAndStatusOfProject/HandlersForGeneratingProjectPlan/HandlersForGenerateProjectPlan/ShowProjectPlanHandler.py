show_plan
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes



from Handlers.Handler import Handler
from Handlers.RequestsHandler import show_plan

class ShowProjectPlanHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    proj_id = context.user_data["chosenProject"]
    plan = show_plan(proj_id)

    keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(plan, reply_markup=reply_markup)
