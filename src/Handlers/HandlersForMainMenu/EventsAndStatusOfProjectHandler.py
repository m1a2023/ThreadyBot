from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class EventsAndStatusOfProjectHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
      [InlineKeyboardButton("Текущие задачи", callback_data="currentTasks")],
      [InlineKeyboardButton("Отчеты (не работает)", callback_data="reportsMenu")],
      [InlineKeyboardButton("План, созданный нейросетью (Не работает)", callback_data="Plan")],
      [InlineKeyboardButton("Выход в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Ближайшие события и состояние проекта. Выберите действие:", reply_markup=reply_markup)
