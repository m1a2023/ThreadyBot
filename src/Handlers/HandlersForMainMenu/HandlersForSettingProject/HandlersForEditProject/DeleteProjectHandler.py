from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from Handlers.RequestsHandler import deleteProject

class DeleteProjectHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    projectId = context.user_data["chosenProject"]
    await deleteProject(projectId)
    
    return await SettingsOfProjectsHandler.handle(update, context)
