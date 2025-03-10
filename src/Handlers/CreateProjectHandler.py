from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

class CreateProjectHandler(Handler):
  @staticmethod
  async def handle(
      update: Update,
      context: ContextTypes.DEFAULT_TYPE
  ) -> Any:  
    
    """ TODO: 
    ask: 
    1) project name
    2) project description
    3) if there is repo link it 
    
    create: 
    1) developers chat"""
    pass