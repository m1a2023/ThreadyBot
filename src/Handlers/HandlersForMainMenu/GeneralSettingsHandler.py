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
      [InlineKeyboardButton("Настроить ссылку на общий чат (Не работает)", callback_data="123")],
      [InlineKeyboardButton("Настроить уведомления о дедлайнах (Не работает)", callback_data="123")],
      [InlineKeyboardButton("Выход в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Общие настройки бота. Выберите действие:", reply_markup=reply_markup)