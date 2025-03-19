from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from TaskManagement.TaskManager import TaskManager

import re
class TextHandler:
  @staticmethod
  async def processMessage(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    user_message_id: int,
    bot_message_id: int,
    new_info: str,
    info_key: str = None
  ):
      # Удаляем предыдущее сообщение бота
      if bot_message_id:
        await context.bot.delete_message(chat_id, bot_message_id)

      # Удаляем сообщение пользователя
      if user_message_id:
        try:
          await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
          print(f"Ошибка при удалении сообщения пользователя: {e}")

      # Удаляем сообщение, чтобы вывести другое с доп. инфой, которую ввел пользователь
      last_bot_message_id = context.user_data.get("IdLastMessageFromBot")
      if last_bot_message_id:
        try:
          await context.bot.delete_message(chat_id, last_bot_message_id)
        except Exception as e:
          print(f"Ошибка при удалении последнего сообщения бота: {e}")

      # Обновляем информацию о проекте
      context.user_data[info_key].append(new_info)

      # Отправляем новое сообщение с обновленной информацией
      last_message_from_bot = await context.bot.send_message(chat_id, "\n".join(context.user_data[info_key]))

      # Сохраняем ID нового сообщения бота
      context.user_data["IdLastMessageFromBot"] = last_message_from_bot.message_id

      # Сбрасываем состояние
      context.user_data["state"] = None

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if "project" in context.user_data:
      project = context.user_data["project"]

    chat_id = update.message.chat_id
    user_message_id = update.message.message_id
    bot_message_id = context.user_data.get("bot_message_id")

    # Получаем текущее состояние
    state = context.user_data.get("state")

    if state == "setNameForCreateProject":
      # Требования к названию проекта: длина названия не менее 4 символов и не должно начинаться с цифры
      # Если ввод корректен, обновляем информацию
      if (len(user_text) >= 4 and not user_text[0].isdigit()):
        project.set_name(user_text)
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Имя проекта: {user_text}", "projectInfoForCreateProject"
        )

        # Сохраняем id пользователя как владельца проекта
        project.set_id_owner(update.message.from_user.id)

      else:
        # Если ввод некорректный, то сообщаем об этом пользователю и запрашиваем ввод снова
        # Редактируем предыдущее сообщение бота
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="Вы ввели некорректное название проекта: имя проекта не может короче 4 символов и не может начинаться с числа.\nВведите имя еще раз:"
            )
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        # Удаляем сообщение пользователя
        if user_message_id:
          try:
            await context.bot.delete_message(chat_id, user_message_id)
          except Exception as e:
            print(f"Ошибка при удалении сообщения пользователя: {e}")
        return

    elif state == "setDescriptionForCreateProject":
      # Удаляем из ввода все, что не буквы и не цифры и разделяем по пробелам
      description = (re.sub(r'[^\w\s]', '', user_text)).split()
      # Описание должно быть не меньше 4 слов
      if len(description) >= 4:
        # Если ввод корректен, обновляем информацию
        project.set_description(user_text)
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Описание проекта: {user_text}", "projectInfoForCreateProject"
        )
      else:
        # Редактируем предыдущее сообщение бота
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="Вы ввели некорректное описание. Описание проекта не может быть меньше 4 слов. Введите описание еще раз:"
            )
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        # Удаляем сообщение пользователя
        try:
          await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
          print(f"Ошибка при удалении сообщения пользователя: {e}")
        return

    elif state == "setTeamForCreateProject":
      # Множество с юзернеймами, введеными от пользвателя
      set_of_team = set((re.sub(r'[^\w\s@]', '', user_text)).split())
      # Добавляем юзернейм создателя, если оно есть, если нет - имя
      if update.message.from_user.username:
        set_of_team.add("@" + update.message.from_user.username)
      else:
        set_of_team.add(update.message.from_user.full_name)

      project.set_team(set_of_team)
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Группа разработчиков: {', '.join(set_of_team)}", "projectInfoForCreateProject"
      )

    elif state == "setLinkForCreateProject":
      # Проверка на то, что это действительно ссылка
      parsed_url = urlparse(user_text)
      if (all([parsed_url.scheme, parsed_url.netloc])):
        project.set_link_rep(user_text)
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Ссылка на репозиторий: {user_text}", "projectInfoForCreateProject"
        )
      else:
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="Введенная ссылка недействительна. Попробуйте еще раз:"
            )
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        # Удаляем сообщение пользователя
        try:
          await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
          print(f"Ошибка при удалении сообщения пользователя: {e}")
        return


    #TASKS
    if "task" in context.user_data:
      task = context.user_data["task"]

    if state == "setNameForTask":
      task.set_name(user_text)
      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Имя задачи: {user_text}", "taskInfoForCreateTask"
        )

    elif state == "setDescriptionForTask":
      task.set_description(user_text)
      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Описание задачи: {user_text}", "taskInfoForCreateTask"
        )

    elif state == "setDeadlineForTask":
      task.set_deadline(user_text)
      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Дедлайн задачи: {user_text}", "taskInfoForCreateTask"
        )

    elif state == "setPriorityForTask":
      task.set_priority(user_text)
      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Приоритет задачи: {user_text}", "taskInfoForCreateTask"
        )

    elif state == "setStatusForTask":
      task.set_status(user_text)
      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Статус задачи: {user_text}", "taskInfoForCreateTask"
        )

    elif state == "deleteTask":
      await context.user_data["task_manager"].delete_task(user_text, update, context)
      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"{user_text}", "taskInfoForDeleteTask"
        )

    elif state == "editTask":
      sent_message=""
      if context.user_data["task_manager"].found_task(user_text,update,context):
          context.user_data["task_name"] = user_text
          keyboard = [
              [InlineKeyboardButton("Изменить имя", callback_data="editTaskName")],
              [InlineKeyboardButton("Изменить описание", callback_data="editTaskDescription")],
              [InlineKeyboardButton("Изменить дедлайн", callback_data="editTaskDeadline")],
              [InlineKeyboardButton("Изменить приоритет", callback_data="editTaskPriority")],
              [InlineKeyboardButton("Изменить статус", callback_data="editTaskStatus")],
              [
                  InlineKeyboardButton("Отмена", callback_data="edit_cancel"),
                  InlineKeyboardButton("Готово", callback_data="edit_done")
              ]
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          #вот тут надо адаптировать под метод process message
          sent_message=await update.message.reply_text(f"Вы выбрали для редактирования задачу: {user_text}\nВыберите действие:",reply_markup=reply_markup)
      else:
          sent_message=await update.message.reply_text("Такой задачи нет")
      context.user_data["bot_message_id"] = sent_message.message_id

      """await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Имя задачи: {user_text}", "taskInfoForCreateTask"
        )"""

    elif state == "editTaskName":
      print(context.user_data["task_name"])
      context.user_data["task_manager"].found_task(context.user_data["task_name"],update,context).set_name(user_text)
      context.user_data["task_name"] = user_text

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Имя задачи: {user_text}", "taskInfoForEditTask"
        )

    elif state == "editTaskDescription":
      context.user_data["task_manager"].found_task(context.user_data["task_name"],update,context).set_description(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Описание задачи: {user_text}", "taskInfoForEditTask"
        )

    elif state == "editTaskDeadline":
      context.user_data["task_manager"].found_task(context.user_data["task_name"],update,context).set_deadline(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Дедлайн задачи: {user_text}", "taskInfoForEditTask"
        )

    elif state == "editTaskPriority":
      context.user_data["task_manager"].found_task(context.user_data["task_name"],update,context).set_priority(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Приоритет задачи: {user_text}", "taskInfoForEditTask"
        )

    elif state == "editTaskStatus":
      context.user_data["task_manager"].found_task(context.user_data["task_name"],update,context).set_status(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Статус задачи: {user_text}", "taskInfoForEditTask"
        )

    # TEAM
    if "team" in context.user_data:
      team = context.user_data["team"]
    
    if state == "addNewDeveloper":
      # Если нет такого пользователя в списке тимы
      if user_text not in team:
        team.append(user_text)
        # Удаляем сообщение бота
        if bot_message_id:
          await context.bot.delete_message(chat_id, bot_message_id)

        # Удаляем сообщение пользователя
        if user_message_id:
          try:
            await context.bot.delete_message(chat_id, user_message_id)
          except Exception as e:
            print(f"Ошибка при удалении сообщения пользователя: {e}")
        
        context.user_data["state"] = None
        
      # Если такой пользователь уже есть в тиме
      else:
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=bot_message_id,
            text="Такой пользователь уже есть в команде. Попробуйте еще раз:"
          )
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
          # Удаляем сообщение пользователя
          if user_message_id:
            try:
              await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
              print(f"Ошибка при удалении сообщения пользователя: {e}")
        return
        
    elif state == "deleteDeveloper":
      try:
        team.remove(user_text)
        # Удаляем сообщение бота
        if bot_message_id:
          await context.bot.delete_message(chat_id, bot_message_id)

        # Удаляем сообщение пользователя
        if user_message_id:
          try:
            await context.bot.delete_message(chat_id, user_message_id)
          except Exception as e:
            print(f"Ошибка при удалении сообщения пользователя: {e}")
        
        context.user_data["state"] = None
        
      except ValueError as e:
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
            chat_id=chat_id,
            message_id=bot_message_id,
            text="Такого пользователя нет в команде. Попробуйте еще раз:"
          )
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
          # Удаляем сообщение пользователя
          if user_message_id:
            try:
              await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
              print(f"Ошибка при удалении сообщения пользователя: {e}")
        return