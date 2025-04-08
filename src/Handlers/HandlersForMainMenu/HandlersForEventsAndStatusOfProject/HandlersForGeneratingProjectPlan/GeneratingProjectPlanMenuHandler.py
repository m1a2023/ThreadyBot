from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes



from Handlers.Handler import Handler

class GeneratingPlanMenuHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
      [InlineKeyboardButton("🔍 Посмотреть план", callback_data="showPlan")],
      [InlineKeyboardButton("🆕 Сгенерировать план", callback_data="generateNewPlan")],
      [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("*\=\=План, созданный нейросетью\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")