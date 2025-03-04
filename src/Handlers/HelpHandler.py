from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class HelpHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> any: 
    user = update._effective_user
    await update.message.reply_html(
        "Available commands: " + \
        "\n/start - run Thready " + \
        "\n/help - show Thready available commands " + \
        "\n/end - stop Thready",
        reply_markup=ForceReply(selective=True),
    )