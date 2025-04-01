from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from ProjectManagment.Project import Project

from Handlers.Handler import Handler

class CreateProjectHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if "Project" not in context.user_data:
      """ Эта штука будет сохранять в контексте инфу о проекте при создании для сохранения в бд """
      context.user_data["project"] = Project()
      """ Эти штуки нужны для красивого вывода (комментариев для пользователя) при создании проекта """
      context.user_data["projectInfoForCreateProject"] = ["Вы ввели:"]

    keyboard = [
      [InlineKeyboardButton("🏷️ Добавить название", callback_data="setNameForCreateProject")],
      [InlineKeyboardButton("📝 Добавить описание", callback_data="setDescriptionForCreateProject")],
      [InlineKeyboardButton("🧑‍💻 Добавить разработчиков", callback_data="setTeamForCreateProject")],
      [InlineKeyboardButton("📎 Добавить ссылку на репозиторий", callback_data="setLinkForCreateProject")],
      [
        InlineKeyboardButton("❌ Отмена", callback_data="CancelCreateProject"),
        InlineKeyboardButton("✅ Создать", callback_data="SaveNewProject")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с кнопками
    await query.edit_message_text("*\=\=Создание проекта\=\=*\nДобавьте информацию о новом проекте:", reply_markup=reply_markup, parse_mode="MarkdownV2")



















  # CREATE, NAME, DESCRIPTION, DEVELOPERS, LINK = range(5)  # States for ConversationHandler

  # def __init__(self):
  #     self.about_project = {"name": "", "description": "","developers": [],"linkRep": ""}  # Variable for storing data about project

  # """ Start of create """
  # async def create(self, update: Update, context: CallbackContext) -> int:
  #     await update.message.reply_text("Name of this project?")
  #     return self.NAME

  # """ Project name """
  # async def name(self, update: Update, context: CallbackContext):
  #     self.about_project["name"] = update.message.text
  #     await update.message.reply_text("Do you provide some description? If yes, write it, else write \"skip\"")
  #     return self.DESCRIPTION

  # """ Project description """
  # async def description(self, update: Update, context: CallbackContext):
  #     description_text = update.message.text
  #     if description_text.lower() == "skip":
  #       self.about_project["description"] = ""
  #     else:
  #        self.about_project["description"] = description_text

  #     username = update.message.from_user.username
  #     await update.message.reply_text("Want to add developers to the project?"
  #     "\nIf yes, write their nicknames, if no, then write \"skip\""
  #     "\nFor example: @" + username + ", @123 and etc")

  #     return self.DEVELOPERS

  # """ Add developers """
  # async def developers(self, update: Update, context: CallbackContext):
  #   developers_list = update.message.text
  #   if developers_list.lower() == "skip":
  #       self.about_project["developers"] = ""
  #   else:
  #      self.about_project["developers"] = developers_list.split(", ")

  #   await update.message.reply_text("If there is a repo link, send it, if not, skip it (send \"skip\")")
  #   return self.LINK

  # """ Check of url """
  # @staticmethod
  # def is_valid_url(url):
  #   parsed_url = urlparse(url)
  #   return all([parsed_url.scheme, parsed_url.netloc])

  # """ Repo link """
  # async def link(self, update: Update, context: CallbackContext):
  #     link_text = update.message.text
  #     if link_text.lower() == 'skip':
  #         self.about_project["linkRep"] = ""
  #     else:
  #       if self.is_valid_url(link_text):
  #         self.about_project["linkRep"] = link_text
  #       else:
  #          await update.message.reply_text("The entered message is not a link. Repeat entry")
  #          return self.LINK

  #     await update.message.reply_text("The project has been created\n\n" + str(self.about_project))
  #     return ConversationHandler.END

  # """ Cancel of create project """
  # async def cancel(self, update: Update, context: CallbackContext):
  #   await update.message.reply_text("Project creation canceled")
  #   return ConversationHandler.END
