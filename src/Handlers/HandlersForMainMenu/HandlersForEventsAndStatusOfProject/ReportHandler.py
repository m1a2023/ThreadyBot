from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class ReportMenuHandler(Handler): 
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    await query.answer()

    keyboard = [
      [InlineKeyboardButton("Сделать отчет по сотрудникам (Не работает)", callback_data="123")],
      [InlineKeyboardButton("Сделать отчет о ходе выполнения задач (Не работает)", callback_data="123")],
      [InlineKeyboardButton("Выход в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Генерация отчетов. Выберите вид отчетов:", reply_markup=reply_markup)