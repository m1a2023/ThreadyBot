from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from ProjectManagment.ProjectManager import ProjectManager

class SettingsOfProjectsHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    await ProjectManager.get_and_update_list_projects(update, context)

    keyboard = [
      [InlineKeyboardButton("Создание нового проекта", callback_data="CreateProject")],
      [InlineKeyboardButton("Изменить сущеcтвующий проект", callback_data="ChangeProject")],
      [InlineKeyboardButton("Посмотреть данные о проекте", callback_data="ShowProjectsInfo")],
      [InlineKeyboardButton("Удалить проект",callback_data="ConfirmationDeleteProject")],
      [InlineKeyboardButton("Выйти в главное меню", callback_data="MoveToMainMenu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Управление проектами. Выберите действие", reply_markup=reply_markup)
