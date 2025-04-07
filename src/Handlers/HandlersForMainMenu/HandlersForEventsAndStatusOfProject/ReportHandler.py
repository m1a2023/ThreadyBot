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
      [InlineKeyboardButton("🧑‍💻 Сделать отчет по сотруднику", callback_data="get_developer_report")],
      [InlineKeyboardButton("📈 Сделать отчет о проекте", callback_data="get_project_report")],
      [InlineKeyboardButton("🏠 Выход в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("*\=\=Генерация отчетов\=\=*\nВыберите вид отчетов:", reply_markup=reply_markup, parse_mode="MarkdownV2")
