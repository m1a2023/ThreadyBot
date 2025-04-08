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
      [InlineKeyboardButton("📌 Текущие задачи", callback_data="currentTasks")],
      [InlineKeyboardButton("🧑‍💻 Просмотр данных о команде", callback_data="showTeam")],
      [InlineKeyboardButton("📊 Отчеты", callback_data="reportsMenu")],
      # [InlineKeyboardButton("🤖 План, созданный нейросетью", callback_data="Plan")],
      [InlineKeyboardButton("🤖 План, созданный нейросетью", callback_data="GeneratingPlanMenu")],
      [InlineKeyboardButton("🏠 Выход в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("*\=\=Состояние проекта\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")
