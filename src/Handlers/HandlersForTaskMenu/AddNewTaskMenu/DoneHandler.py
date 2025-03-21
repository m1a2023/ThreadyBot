from telegram import Update
from telegram.ext import ContextTypes

from typing import Any

from telegram.error import BadRequest

from Handlers.Handler import Handler

from Handlers.HandlersForTaskMenu.AddNewTaskMenu.NameHandler import NameHandler
from Handlers.HandlersForTaskMenu.AddNewTaskMenu.DescriptionHandler import DescriptionHandler
from Handlers.HandlersForTaskMenu.MainTaskMenuHandler import MainTaskMenuHandler

class DoneHandler(Handler):
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
    keys_for_check = ["name", "description"]
    for key in keys_for_check:
      print("проверка")
      if new_task[key] == None:
        if key == "name":
          print("проверку не прошло имя")
          await context.bot.send_message(chat_id=chat_id, text="Вы забыли ввести имя задачи")
          #context.user_data["state"] = "setNameForTask"
          return await NameHandler.handle(update, context)
        elif key == "description":
          print("проверку не прошло описание")
          await context.bot.send_message(chat_id=chat_id, text="Вы забыли добавить описание проекту")
          #context.user_data["state"] = "setDescriptionForTask"
          return await DescriptionHandler.handle(update, context)

    task_manager = context.user_data["task_managers"].get(context.user_data["project_name"])

    if task_manager:
        await task_manager.add_task(update, context)
    else:
        print("Ошибка: TaskManager для текущего проекта не найден!")


    #await context.user_data["task_manager"].add_task(update, context)

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
