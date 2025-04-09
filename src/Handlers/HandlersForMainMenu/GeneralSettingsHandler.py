from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class GeneralSettingsHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    keyboard = [
      [InlineKeyboardButton("📎 Настроить ссылку на общий чат", callback_data="setChatLink")],
      [InlineKeyboardButton("🔍 Посмотреть ссылку на общий чат", callback_data="showChatLink")],
      [InlineKeyboardButton("🏠 Выход в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("*\=\=Общие настройки бота\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")
