from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes



from Handlers.Handler import Handler

from LLMgen.GeneratePlan import generateProjectPlan


class GeneratingPlanMenuHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
      [InlineKeyboardButton("Сгенерировть(перегенерировать) план", callback_data="generate_plan")],
      [InlineKeyboardButton("Посмотреть текущий", callback_data="show_current_plan")],
      [InlineKeyboardButton("Назад", callback_data="EventsAndStatusOfProjects")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    #plan = await generateProjectPlan()

    await query.edit_message_text(f"Работа с генерацией плана: ", reply_markup=reply_markup)