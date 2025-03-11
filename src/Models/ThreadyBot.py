from Handlers.StartHandler import StartHandler
from Handlers.HelpHandler import HelpHandler
from Handlers.EndHandler import EndHandler
from Handlers.TaskHandler import TaskHandler
from Models.Bot import Bot

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

"""
  Class methods are representation of bot commands.
  Inherited from abstract class 'Bot'.
"""
class ThreadyBot(Bot):
  """
  Command "start" representation in ThreadyBot.
  Any data will send to handle and will handled in StartHandler.
  """
  async def start(
      self,
      update: Update,
      context: ContextTypes.DEFAULT_TYPE
      ) -> None:
    await StartHandler.handle(update, context)

  """
  Command "end" representation in ThreadyBot.
  Any data will send to handle and will handled in EndHandler.
  """
  async def end(
      self,
      update: Update,
      context: ContextTypes.DEFAULT_TYPE
      ) -> None:
    await EndHandler.handle(update, context)

  """
  Command "help" representation in ThreadyBot.
  Any data will send to handle and will handled in HelpHandler.
  """
  async def help(
      self,
      update: Update,
      context: ContextTypes.DEFAULT_TYPE
  ) -> None:
    await HelpHandler.handle(update, context)

  async def create_project(
      self,
      update: Update,
      context: ContextTypes.DEFAULT_TYPE
  ) -> None:
    pass

  async def task_menu(self,
      update: Update,
      context: ContextTypes.DEFAULT_TYPE
      ) -> None:
    await TaskHandler.handle(update, context)
