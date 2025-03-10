from abc import ABC, abstractmethod

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from typing import Any

class Handler(ABC):
  @staticmethod
  @abstractmethod
  async def handle(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
    ) -> Any: pass