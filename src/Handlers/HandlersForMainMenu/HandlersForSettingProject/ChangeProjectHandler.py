from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class ChangeProjectHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    #query = update.callback_query
    #await query.answer()

    keyboard = [
        [InlineKeyboardButton("Изменение задач", callback_data="changeTasks")],
        [InlineKeyboardButton("Изменение данных о команде", callback_data="changeTeam")],
        [InlineKeyboardButton("Изменение данных проекта", callback_data="editProject")],
        [InlineKeyboardButton("Отмена", callback_data="SettingsOfProjects")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Изменение существующего проекта. Выберите действие", reply_markup=reply_markup)
    #await query.edit_message_text("Изменение существующего проекта. Выберите действие", reply_markup=reply_markup)
