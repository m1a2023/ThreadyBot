from Handlers.StartHandler import StartHandler
from Handlers.HelpHandler import HelpHandler
from Handlers.EndHandler import EndHandler
from Handlers.HandlersForTaskMenu.MainTaskMenuHandler import MainTaskMenuHandler
from Models.Bot import Bot

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


from apscheduler.schedulers.asyncio import AsyncIOScheduler

from RemindersHandler import RemindersHandler

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
    # Create scheduler
    scheduler = AsyncIOScheduler()

    scheduler.add_job(RemindersHandler.handle, "interval", seconds=30, args=[update, context])
    scheduler.start()
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

  async def task_menu(
      self,
      update: Update,
      context: ContextTypes.DEFAULT_TYPE
      ) -> None:
    await MainTaskMenuHandler.handle(update, context)
