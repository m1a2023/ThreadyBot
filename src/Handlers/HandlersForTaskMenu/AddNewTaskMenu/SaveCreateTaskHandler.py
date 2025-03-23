from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from telegram.error import BadRequest

from Handlers.Handler import Handler

from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetDeadlineForCreateTaskHandler import SetDeadlineForCreateTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetNameHandler import SetNameTaskHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.SetDescriptionForCreateTaskHandler import SetDescriptionForCreateTaskHandler
from Handlers.HandlersForTaskMenu.MainTaskMenuHandler import MainTaskMenuHandler
from Handlers.RequestsHandler import createTask

class SaveCreateTaskHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Получаем chat_id
    if update.message:
      chat_id = update.message.chat_id
    else:
      chat_id = update.callback_query.message.chat_id

    last_bot_message_id = context.user_data.get("IdLastMessageFromBot")

    # Проверка на то, что пользователь точно ввел имя и описание задачи
    new_task = context.user_data["task"].to_dict()
    keys_for_check = ["title", "description", "deadline"]
    for key in keys_for_check:
      if new_task[key] == None:
        if key == "title":
          await context.bot.editMessageText(chat_id=chat_id, message_id=last_bot_message_id, text="Вы забыли ввести имя задачи")
          context.user_data["state"] = "setNameForTask"
          return await SetNameTaskHandler.handle(update, context)
        elif key == "description":
          await context.bot.editMessageText(chat_id=chat_id, message_id=last_bot_message_id, text="Вы забыли добавить описание задаче")
          context.user_data["state"] = "setDescriptionForTask"
          return await SetDescriptionForCreateTaskHandler.handle(update, context)
        elif key == "deadline":
          message = await context.bot.editMessageText(chat_id=chat_id, message_id=last_bot_message_id, text="Вы забыли добавить дедлайн задаче")
          context.user_data["state"] = "setDeadlineForTask"
          # context.user_data["IdLastMessageFromBot"] = message.id
          # context.user_data["bot_message_id"] = message.id
          return await SetDeadlineForCreateTaskHandler.handle(update, context)
    
    # Сохраняем задачу
    new_task = context.user_data["task"]
    project_id = context.user_data["chosenProject"]
    await createTask(new_task, project_id)

    # Удаляем последнее сообщение бота (если есть)
    if last_bot_message_id:
      try:
        await context.bot.delete_message(chat_id, last_bot_message_id)
      except BadRequest as e:
        print(f"Ошибка при удалении последнего сообщения бота: {e}")

    # Очищаем все данные, связанные с созданием задачи
    keys_to_remove = [
      "state",
      "task",
      "taskInfoForCreateTask",
      "IdLastMessageFromBot",
      "bot_message_id"
    ]
    for key in keys_to_remove:
      if key in context.user_data:
        del context.user_data[key]

    return await MainTaskMenuHandler.handle(update, context)
