from abc import ABC, abstractmethod

from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class Bot(ABC):

  @abstractmethod
  async def start(
    self, update: Update, context: ContextTypes.DEFAULT_TYPE 
    ) -> None: pass

  # @abstractmethod
  # async def end(
  #   self, update: Update, context: ContextTypes.DEFAULT_TYPE 
  #   ) -> None: pass
  
  # @abstractmethod
  # async def help(
  #   self, update: Update, context: ContextTypes.DEFAULT_TYPE 
  #   ) -> None: pass

