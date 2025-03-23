from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes



from Handlers.Handler import Handler

class GeneratingPlanMenuHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
      [InlineKeyboardButton("Сгенерировть новый план", callback_data="generate_plan")],
      [InlineKeyboardButton("Посмотреть текущий", callback_data="get_project_report")],
      [InlineKeyboardButton("Назад", callback_data="EventsAndStatusOfProjects")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Работа с генерацией плана:", reply_markup=reply_markup)