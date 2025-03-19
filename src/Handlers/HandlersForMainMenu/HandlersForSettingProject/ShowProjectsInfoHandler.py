from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

class ShowProjectsInfoHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    await context.user_data["project_manager"].show_projects(update, context)
