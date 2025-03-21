from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetDescriptionHandler import SetDescriptionHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForCreateProject.SetNameHandler import SetNameHandler
from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from telegram.error import BadRequest

from Handlers.Handler import Handler

from TaskManagement.TaskManager import TaskManager

from Handlers.RequestsHandler import saveNewProject

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

    id_proj = await saveNewProject(new_project)
    
    
    
    # await context.user_data["project_manager"].add_project(update, context)

    # if "task_managers" not in context.user_data:
    #     context.user_data["task_managers"] = {}

    # project_name = context.user_data["project_name"]  # Имя текущего проекта

    # if project_name not in context.user_data["task_managers"]:
    #     context.user_data["task_managers"][project_name] = TaskManager()


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
