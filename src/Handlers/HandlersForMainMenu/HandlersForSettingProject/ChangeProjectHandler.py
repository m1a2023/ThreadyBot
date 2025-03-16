from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class ChangeProjectHandler(Handler): 

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("Изменение задач (пока не работает)", callback_data="123")],
        [InlineKeyboardButton("Изменение данных о команде (не работает)", callback_data="123")],
        [InlineKeyboardButton("Изменение данных проекта (не работает)", callback_data="123")],
        [InlineKeyboardButton("Отмена", callback_data="SettingsOfProjects")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Изменение существующего проекта. Выберите действие", reply_markup=reply_markup)