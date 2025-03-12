from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from urllib.parse import urlparse

class CreateProjectHandler: 
  """ States for ConversationHandler """
  CREATE, NAME, DESCRIPTION, DEVELOPERS, LINK = range(5)

  def __init__(self):
      self.about_project = {"name": "", "description": "","developers": [],"linkRep": ""}
  
  """ Start of create """
  async def create(self, update: Update, context: CallbackContext) -> int:
      await update.message.reply_text("Name of this project?")
      return self.NAME

  """ Project name """ 
  async def name(self, update: Update, context: CallbackContext):
      self.about_project["name"] = update.message.text
      await update.message.reply_text("Do you provide some description? If yes, write it, else write \"skip\"")
      return self.DESCRIPTION

  """ Project description """
  async def description(self, update: Update, context: CallbackContext):
      description_text = update.message.text
      if description_text.lower() == "skip":
        self.about_project["description"] = ""
      else:
         self.about_project["description"] = description_text

      await update.message.reply_text("Want to add developers to the project?"
      "\nIf yes, write their nicknames with a space, if no, then write \"skip\"")      
      return self.DEVELOPERS
  
  """ Add developers """
  async def developers(self, update: Update, context: CallbackContext):
    developers_list = update.message.text
    if developers_list.lower() == "skip":
        self.about_project["developers"] = ""
    else:
       self.about_project["developers"] = developers_list.split()

    await update.message.reply_text("If there is a repo link, send it, if not, skip it (send \"skip\")")
    return self.LINK

  """ Check of url """
  @staticmethod
  def is_valid_url(url):
    parsed_url = urlparse(url)
    return all([parsed_url.scheme, parsed_url.netloc])
  
  """ Repo link """
  async def link(self, update: Update, context: CallbackContext):
      link_text = update.message.text
      if link_text.lower() == 'skip':
          self.about_project["linkRep"] = ""
      else:
        if self.is_valid_url(link_text):
          self.about_project["linkRep"] = link_text
        else:
           await update.message.reply_text("The entered message is not a link. Repeat entry")
           return self.LINK
      
      await update.message.reply_text("The project has been created\n\n" + str(self.about_project))
      return ConversationHandler.END
  
  """ Cancel of create project """
  async def cancel(self, update: Update, context: CallbackContext):
    await update.message.reply_text("Project creation canceled")
    return ConversationHandler.END
  
# Как использовать (для main)
# CreateProject = CreateProjectHandler()
#     CreateProject_handler = ConversationHandler(
#         entry_points=[CommandHandler('CreateProject', CreateProject.create)], 
#         states={
#             CreateProject.CREATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.create)],
#             CreateProject.NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.name)],
#             CreateProject.DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.description)],
#             CreateProject.DEVELOPERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.developers)],
#             CreateProject.LINK: [MessageHandler(filters.TEXT & ~filters.COMMAND, CreateProject.link)],
#         }, 
#         fallbacks=[CommandHandler('cancel', CreateProject.cancel)],
#     )