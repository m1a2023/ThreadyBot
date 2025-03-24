from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getProjectById
from ProjectManagment.ProjectManager import ProjectManager

class ShowProjectsInfoHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    await ProjectManager.get_and_update_list_projects(update, context)

    chosenProj = context.user_data["chosenProject"]

    foundProject = await getProjectById(int(chosenProj))

    keyboard = [
      [InlineKeyboardButton("Назад", callback_data="SettingsOfProjects")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"Данные о проекте:\n{foundProject.__str__()}", reply_markup=reply_markup)
    
    context.user_data["chosenProject"] = None
