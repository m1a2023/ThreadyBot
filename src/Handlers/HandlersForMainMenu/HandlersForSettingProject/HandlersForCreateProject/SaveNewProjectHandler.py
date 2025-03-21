from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetDescriptionHandler import SetDescriptionHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetNameHandler import SetNameHandler
from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from telegram.error import BadRequest

from Handlers.Handler import Handler

from ProjectManagment.Developer import Developer

from Handlers.RequestsHandler import addUserToTeam, createNewTeams, saveNewProject

class SaveCreateProjectHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем chat_id
    if update.message:
      chat_id = update.message.chat_id
    else:
      chat_id = update.callback_query.message.chat_id

    last_bot_message_id = context.user_data.get("IdLastMessageFromBot")

    # Проверка на то, что пользователь точно ввел имя и описание проекта
    new_project = context.user_data["project"].to_dict()
    keys_for_check = ["title", "description"]
    for key in keys_for_check:
      if new_project[key] == "":
        if key == "title":
          await context.bot.editMessageText(chat_id=chat_id, message_id=last_bot_message_id, text="Вы забыли ввести имя проекта")
          context.user_data["state"] = "setNameForCreateProject"
          return await SetNameHandler.handle(update, context)
        elif key == "description":
          await context.bot.editMessageText(chat_id=chat_id, message_id=last_bot_message_id, text="Вы забыли добавить описание проекту")
          context.user_data["state"] = "setDescriptionForCreateProject"
          return await SetDescriptionHandler.handle(update, context)

    # Сохраняем проект
    project_id = await saveNewProject(new_project)

    # Добавляем владельца в команду (и создаем команду)
    owner = Developer(update.callback_query.message.chat_id, project_id, "admin")
    await createNewTeams(owner.to_dict())

    # Добавляем разрабов
    for developer in new_project["team"]:
      developer["project_id"] = project_id
      await addUserToTeam(developer)

    # Удаляем последнее сообщение бота (если есть)
    if last_bot_message_id:
      try:
        await context.bot.delete_message(chat_id, last_bot_message_id)
      except BadRequest as e:
        print(f"Ошибка при удалении последнего сообщения бота: {e}")

    # Очищаем все данные, связанные с созданием проекта
    keys_to_remove = [
      "state",
      "project",
      "projectInfoForCreateProject",
      "IdLastMessageFromBot",
      "bot_message_id"
    ]
    for key in keys_to_remove:
      if key in context.user_data:
        del context.user_data[key]

    return await SettingsOfProjectsHandler.handle(update, context)
