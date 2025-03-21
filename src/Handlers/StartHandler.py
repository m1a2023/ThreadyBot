from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

from Handlers.MainMenuHandler import MainMenuHandler

from Handlers.RequestsHandler import *

class StartHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any: 
    if update.message and update.effective_user:
      user = update.effective_user 
      await update.message.reply_html(
          rf"Привет, {user.mention_html()}!"
      )
    
    # Если юзера нет в базе, то добавляем
    if not await checkUserExists(int(update.message.from_user.id)):
      await addNewUser(update.message.from_user.id, update.message.from_user.full_name)

    """ Вызов главного меню """
    return await MainMenuHandler.handle(update, context)