from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

class EndHandler(Handler):
  @staticmethod
  async def handle(update: Update, context:  ContextTypes.DEFAULT_TYPE) -> any:
    user = update.effective_user
    await update.message.reply_html(
      rf"Bye, {user.mention_html()}",
      reply_markup=ForceReply(selective=True)
    ) 
    await context.application.stop();