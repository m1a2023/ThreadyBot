""" Python general packages """
import sys as system
import logging
from typing import Any
""" Python-telegram-bot packages """
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler, CallbackQueryHandler
""" Thready packages """
from Models.ThreadyBot import ThreadyBot

from Models.bot_app import BotApp
from Handlers.TaskHandler import TaskHandler
from Handlers.TaskMenu.MenuHandler import MenuHandler
from Handlers.TaskMenu.AddHandler import AddHandler
from Handlers.TaskMenu.EditHandler import EditHandler
from Handlers.TaskMenu.DeleteHandler import DeleteHandler
from Handlers.TaskMenu.TextHandler import TextHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
		if update.message:
			await update.message.reply_text("There is no such command")
		elif update.callback_query:
			await update.callback_query.edit_message_text("There is no sucn command")

class Main:
	@staticmethod
	def main(argv: list[str]) -> None:
		"""Start the bot."""

		# pass telegram token through cmd
		if argv is None:
			logger.critical("You did not provide the API key to the telegram-bot.\n Insert it and try again.")
			return

		TG_TOKEN = argv[0]

		# Create the Application and pass it your bot's token.
		bot_app = BotApp(TG_TOKEN)
		application = bot_app.get_application()


		#TaskHandler.init()


		#Create the Bot
		thready_bot = ThreadyBot()



		# on different commands - answer in Telegram
		application.add_handler(CommandHandler("start", thready_bot.start))
		application.add_handler(CommandHandler("help", thready_bot.help))
		application.add_handler(CommandHandler("end", thready_bot.end))

		application.add_handler(CommandHandler("task_menu", thready_bot.task_menu))
		application.add_handler(CallbackQueryHandler(MenuHandler.handle))

		application.add_handler(CallbackQueryHandler(AddHandler.handle, pattern="add_opt"))
		application.add_handler(CallbackQueryHandler(EditHandler.handle, pattern="edit_opt"))
		application.add_handler(CallbackQueryHandler(DeleteHandler.handle, pattern="del_opt"))

		application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, TextHandler.handle))

		# on non command i.e message - echo the message on Telegram
		application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

		# Run the bot until the user presses Ctrl-C
		application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    Main.main( system.argv[1:] )
