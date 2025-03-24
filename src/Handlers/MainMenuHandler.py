from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

from ProjectManagment.ProjectManager import ProjectManager

class MainMenuHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ProjectManager.get_and_update_list_projects(update, context)

    keyboard = [
      [InlineKeyboardButton("Управление проектами", callback_data="SettingsOfProjects")],
      [InlineKeyboardButton("Ближайшие события и состояние проекта", callback_data="EventsAndStatusOfProjects")],
      [InlineKeyboardButton("Общие настройки", callback_data="GeneralSettings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
      query = update.callback_query
      await query.answer()  # Подтверждаем callback

      # Редактируем сообщение с кнопками
      await query.edit_message_text(text="Главное меню\nВыберите действие", reply_markup=reply_markup)
    else:
      # Отправляем новое сообщение с кнопками
      await update.message.reply_text(text="Главное меню\nВыберите действие", reply_markup=reply_markup)
