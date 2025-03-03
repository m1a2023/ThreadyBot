from Handlers.StartHandler import StartHandler
from Models.Bot import Bot

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class ThreadyBot(Bot):
  async def start(
    self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None: 
    StartHandler.handle(update, context)
  
