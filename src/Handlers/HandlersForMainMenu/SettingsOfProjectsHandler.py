from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class SettingsOfProjectsHandler(Handler): 
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    await query.answer()

    keyboard = [
      [InlineKeyboardButton("Создание нового проекта", callback_data="CreateProject")],
      [InlineKeyboardButton("Изменить сущетсвующий проект", callback_data="ChangeProject")],
      [InlineKeyboardButton("Выйти в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Управление проектами. Выберите действие", reply_markup=reply_markup)