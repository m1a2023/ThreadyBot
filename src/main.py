import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from Models.ThreadyBot import ThreadyBot 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

class Main:
    @staticmethod
    def main() -> None: 
      """Start the bot."""
      # Create the Application and pass it your bot's token.
      application = Application.builder().token("token").build()

			#Create the Bot 
      thready_bot = ThreadyBot()

      # on different commands - answer in Telegram
      application.add_handler(CommandHandler("start", thready_bot.start))
    	#   application.add_handler(CommandHandler("help", help_command))
			#   application.add_handler(CommandHandler("end", end))

      # on non command i.e message - echo the message on Telegram
      application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

      # Run the bot until the user presses Ctrl-C
      application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    Main.main()