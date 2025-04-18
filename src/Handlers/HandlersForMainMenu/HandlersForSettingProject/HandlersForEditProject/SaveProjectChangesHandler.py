from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from telegram.error import BadRequest

from Handlers.Handler import Handler


from Handlers.HandlersForMainMenu.SettingsOfProjectsHandler import SettingsOfProjectsHandler
from Handlers.RequestsHandler import updateProjectById

class SaveProjectChangesHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем chat_id
    if update.message:
      chat_id = update.message.chat_id
    else:
      chat_id = update.callback_query.message.chat_id

    last_bot_message_id = context.user_data.get("IdLastMessageFromBot")

    # Удаляем последнее сообщение бота (если есть)
    if last_bot_message_id:
      try:
        await context.bot.delete_message(chat_id, last_bot_message_id)
      except BadRequest as e:
        print(f"Ошибка при удалении последнего сообщения бота: {e}")

    # Сохраняем изменения
    changed_project = context.user_data["changedProject"].to_dict()
    new_info = {}
    for key in changed_project:
      if changed_project[key] != "":
        new_info[f"{key}"] = changed_project[key]
    await updateProjectById(int(context.user_data["chosenProject"]), new_info)


    # Очищаем все данные, связанные с редактированием задачи
    keys_to_remove = [
      "state",
      "changedProject",
      "projectInfoForChangeProject",
      "IdLastMessageFromBot",
      "bot_message_id"
    ]
    for key in keys_to_remove:
      if key in context.user_data:
        del context.user_data[key]

    return await SettingsOfProjectsHandler.handle(update, context)
