from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

class StartHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any: 
    if update.message and update.effective_user:
      user = update.effective_user 
      await update.message.reply_html(
          rf"Hi {user.mention_html()}!"
      )