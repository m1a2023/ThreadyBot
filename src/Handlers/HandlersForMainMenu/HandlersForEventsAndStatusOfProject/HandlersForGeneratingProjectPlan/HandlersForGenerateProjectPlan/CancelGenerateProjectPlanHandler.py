from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.EventsAndStatusOfProjectHandler import EventsAndStatusOfProjectHandler


class CancelGenerateProjectPlanHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    if "chosenProject" in context.user_data:
      del context.user_data["chosenProject"]
    
    return await EventsAndStatusOfProjectHandler.handle(update, context)