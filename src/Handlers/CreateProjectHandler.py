from Handlers.Handler import Handler

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, ConversationHandler

from typing import Any

class CreateProjectHandler:
  # @staticmethod
  # async def handle(
  #     update: Update,
  #     context: ContextTypes.DEFAULT_TYPE
  # ) -> Any:  
  #   pass
  """ States for ConversationHandler """
  CREATE, NAME, DESCRIPTION, LINK = range(4)

  def __init__(self):
    self.about_project = {"name": "", "description": "", "linkRep": ""}
  
  """ Start of create """
  async def create(self, update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Name of this project?")
    return self.NAME

  """ Project name """ 
  async def name(self, update: Update, context: CallbackContext) -> int:
    self.about_project["name"] = update.message.text
    await update.message.reply_text("Do you provide some description? If yes, write it, else write \"skip\"")
    return self.DESCRIPTION

  """ Project description """
  async def description(self, update: Update, context: CallbackContext) -> int:
    description_text = update.message.text
    if description_text.lower() == "skip":
      self.about_project["description"] = ""
    else:
      self.about_project["description"] = description_text

    await update.message.reply_text("If there is a repo link, send it, if not, skip it (send \"skip\")")
    return self.LINK

  """ Repo link """
  async def link(self, update: Update, context: CallbackContext) -> int:
    link_text = update.message.text
    if link_text.lower() == "skip":
      self.about_project["linkRep"] = ""
    else:
      self.about_project["linkRep"] = link_text
    await update.message.reply_text("The project has been created\n\n" + str(self.about_project))
    return ConversationHandler.END
  
  """ Cancel of create project """
  async def cancel(self, update: Update, context: CallbackContext):
    await update.message.reply_text("Project creation canceled")
    return ConversationHandler.END
  
# Как использовать (для main)
#     CreateProject = CreateProjectHandler()
#     CreateProject_handler = ConversationHandler(
#         entry_points=[CommandHandler('CreateProject', CreateProject.create)], 
#         states={
#             CreateProject.CREATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.create)],
#             CreateProject.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.name)],
#             CreateProject.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.description)],
#             CreateProject.LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.link)],
#         }, 
#         fallbacks=[CommandHandler('cancel', CreateProject.cancel)],
#     )