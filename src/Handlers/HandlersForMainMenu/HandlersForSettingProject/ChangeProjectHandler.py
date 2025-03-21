from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from ProjectManagment.ProjectManager import ProjectManager

class ChangeProjectHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    await ProjectManager.get_and_update_list_projects(update, context)

    keyboard = [
        [InlineKeyboardButton("Изменение задач", callback_data="changeTasks")],
        [InlineKeyboardButton("Изменение данных проекта", callback_data="editProject")],
        [InlineKeyboardButton("Изменение данных о команде", callback_data="changeTeam")],
        [InlineKeyboardButton("Отмена", callback_data="SettingsOfProjects")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text("Изменение существующего проекта. Выберите действие", reply_markup=reply_markup)
