from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

class EndHandler(Handler):
  @staticmethod
  async def handle(update: Update, context:  ContextTypes.DEFAULT_TYPE) -> Any:
    if update.message:
      await update.message.reply_html(
        "Bye!", reply_markup=ForceReply(selective=True)
      ) 
    await context.application.stop()