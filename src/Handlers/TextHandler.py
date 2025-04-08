from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from datetime import datetime, timezone

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.error import BadRequest

from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.EditProjectInfoMenuHandler import EditProjectInfoMenuHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditTaskMenuHandler import EditTaskMenuHandler
from Handlers.HandlersForMainMenu.HandlersForSettingProject.ChangeProjectHandler import ChangeProjectHandler

import re

from Handlers.RequestsHandler import addUserToTeam, deleteUserFromTeam, getListDevelopersIdByProjectId, getProjectById
from ProjectManagment.Developer import Developer

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
    context.user_data["calendar_id"] = None

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
      user_text = update.message.text
      chat_id = update.message.chat_id
      user_message_id = update.message.message_id

    if "project" in context.user_data:
      project = context.user_data["project"]

    bot_message_id = context.user_data.get("bot_message_id")

    if "project_manager" in context.user_data:
      users_project = await context.user_data["project_manager"].get_projects_names()

    if "changedProject" in context.user_data:
      changedProject = context.user_data["changedProject"]

    if "changedTask" in context.user_data:
      changedTask = context.user_data["changedTask"]

    # Получаем текущее состояние
    state = context.user_data.get("state")

    #
    # Обработка статусов для редактирования проектов
    #

    if state == "editProjectName":
      if (len(user_text) >= 4 and not user_text[0].isdigit() and user_text not in users_project):
        changedProject.title = user_text
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Имя проекта: {user_text}", "projectInfoForChangeProject"
        )
      else:
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="Вы ввели некорректное название проекта: имя проекта не может короче 4 символов и не может начинаться с числа. Также, названия проектов не должны повторяться\nВведите имя еще раз:"
            )
            context.user_data["IdLastMessageFromBot"] = bot_message_id
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        # Удаляем сообщение пользователя
        if user_message_id:
          try:
            await context.bot.delete_message(chat_id, user_message_id)
          except Exception as e:
            print(f"Ошибка при удалении сообщения пользователя: {e}")
        return

    elif state == "editProjectDescription":
      description = (re.sub(r'[^\w\s]', '', user_text)).split()
      if len(description) >= 2:
        # Если ввод корректен, обновляем информацию
        changedProject.set_description(user_text)
        print(changedProject.__str__())
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Описание проекта: {user_text}", "projectInfoForChangeProject"
        )
      else:
        # Редактируем предыдущее сообщение бота
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="Вы ввели некорректное описание. Описание проекта не может быть меньше 15 слов. Введите описание еще раз:"
            )
            context.user_data["IdLastMessageFromBot"] = bot_message_id
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        # Удаляем сообщение пользователя
        try:
          await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
          print(f"Ошибка при удалении сообщения пользователя: {e}")
        return

    elif state == "editProjectLink":
      parsed_url = urlparse(user_text)
      if (all([parsed_url.scheme, parsed_url.netloc])):
        changedProject.set_repo_link(user_text)
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Ссылка на репозиторий: {user_text}", "projectInfoForChangeProject"
        )
      else:
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="Введенная ссылка недействительна. Попробуйте еще раз:"
            )
            context.user_data["IdLastMessageFromBot"] = bot_message_id
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        # Удаляем сообщение пользователя
        try:
          await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
          print(f"Ошибка при удалении сообщения пользователя: {e}")
        return

    #
    # Обработка статусов для создания проектов
    #

    elif state == "setNameForCreateProject":
      # Требования к названию проекта: длина названия не менее 4 символов, не должно начинаться с цифры
      # и названия проектов не должны повторяться
      # Если ввод корректен, обновляем информацию
      if (len(user_text) >= 4 and not user_text[0].isdigit() and user_text not in users_project):
        context.user_data["project_name"] = user_text
        project.set_title(user_text)
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Название проекта: {user_text}", "projectInfoForCreateProject"
        )

        # Сохраняем id пользователя как владельца проекта
        project.set_owner_id(update.message.from_user.id)

      else:
        # Если ввод некорректный, то сообщаем об этом пользователю и запрашиваем ввод снова
        # Редактируем предыдущее сообщение бота
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="❌ Вы ввели некорректное название проекта: имя проекта не может быть короче 4 символов или начинаться с числа. Возможно, у вас уже есть проект с таким названием.\nВведите имя еще раз:"
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
      # Описание должно быть не меньше 15 слов
      if len(description) >= 2:
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
              text="❌ Вы ввели некорректное описание. Описание проекта не может быть короче 15 слов.\nВведите описание еще раз:"
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
      set_of_team = set((re.sub(r'[^\w\s@]', '', user_text)).split())
      try:
        for dev_id in set_of_team:
          dev_id_int = int(dev_id)
          developer = Developer(dev_id_int, 0, "user")
          project.addDeveloper(developer)
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Разработчики: {', '.join(set_of_team)}", "projectInfoForCreateProject"
        )
      except ValueError:
        if bot_message_id:
          try:
            await context.bot.edit_message_text(
              chat_id=chat_id,
              message_id=bot_message_id,
              text="❌ Вы ввели неправильный ID.\nВведите данные еще раз:"
            )
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        try:
          await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
          print(f"Ошибка при удалении сообщения пользователя: {e}")

        return

    elif state == "setLinkForCreateProject":
      # Проверка на то, что это действительно ссылка
      parsed_url = urlparse(user_text)
      if (all([parsed_url.scheme, parsed_url.netloc])):
        project.set_repo_link(user_text)
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
              text="❌ Введенная ссылка недействительна. Попробуйте еще раз:"
            )
          except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")
        # Удаляем сообщение пользователя
        try:
          await context.bot.delete_message(chat_id, user_message_id)
        except Exception as e:
          print(f"Ошибка при удалении сообщения пользователя: {e}")
        return

    #
    # Обработка статусов для создания тасков
    #

    if "task" in context.user_data:
      task = context.user_data["task"]

    if state == "setNameForTask":
      task.set_title(user_text)
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
      # Проверяем, есть ли callback_query
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      # Извлекаем дату
      try:
        _, year, month, day = update.callback_query.data.split("_")
        selected_date_str = f"{year}-{month}-{day}"  # Форматируем дату в строку
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
      except ValueError as e:
        await update.callback_query.message.reply_text(f"Ошибка при обработке даты: {e}")
        return

      # Проверяем корректность даты (например, что она не в прошлом)
      if selected_date < datetime.now():
        await update.callback_query.message.reply_text("Выбранная дата уже прошла, повторите выбор")
        return

      task.set_deadline(selected_date_str)

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Дедлайн: {selected_date_str}", "taskInfoForCreateTask")

    elif state == "setPriorityForTask":
      # Проверяем, есть ли callback_query
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      priority = update.callback_query.data[12:]

      task.priority = priority.lower()

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      # Используем метод processMessage для обработки сообщений
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Приоритет: {priority}", "taskInfoForCreateTask")

    elif state == "setStatusForTask":
      # Проверяем, есть ли callback_query
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      status = update.callback_query.data[10:]

      task.status = status.lower()

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      # Используем метод processMessage для обработки сообщений
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Статус: {status}", "taskInfoForCreateTask")

    elif state == "setDeveloperForTask":
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      developer = update.callback_query.data[23:]

      task.developer = developer

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      # Используем метод processMessage для обработки сообщений
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Исполнитель: {developer}", "taskInfoForCreateTask")


    #
    # Обработка статусов для редактирования тасков
    #

    elif state == "editTaskName":
      changedTask.title = user_text

      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Название задачи: {user_text}", "TaskInfoForChangeTask"
      )

    elif state == "editTaskDescription":
      changedTask.description = user_text

      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Описание задачи задачи: {user_text}", "TaskInfoForChangeTask"
      )

    elif state == "editTaskDeadline":
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      # Извлекаем дату
      try:
        _, year, month, day = update.callback_query.data.split("_")
        selected_date_str = f"{year}-{month}-{day}"  # Форматируем дату в строку
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")
      except ValueError as e:
        await update.callback_query.message.reply_text(f"Ошибка при обработке даты: {e}")
        return

      # Проверяем корректность даты (например, что она не в прошлом)
      if selected_date < datetime.now():
        await update.callback_query.message.reply_text("Выбранная дата уже прошла, повторите выбор")
        return

      changedTask.set_deadline(selected_date_str)

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Дедлайн: {selected_date_str}", "TaskInfoForChangeTask")

    elif state == "editTaskPriority":
      # Проверяем, есть ли callback_query
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      priority = update.callback_query.data[12:]

      changedTask.priority = priority.lower()

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      # Используем метод processMessage для обработки сообщений
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Приоритет: {priority}", "TaskInfoForChangeTask")

    elif state == "editTaskStatus":
      # Проверяем, есть ли callback_query
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      status = update.callback_query.data[10:]

      changedTask.status = status.lower()

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      # Используем метод processMessage для обработки сообщений
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Статус: {status}", "TaskInfoForChangeTask")

    elif state == "EditTaskDeveloper":
      # Проверяем, есть ли callback_query
      if not update.callback_query:
        await update.message.reply_text("Ошибка: callback_query отсутствует.")
        return

      developer = update.callback_query.data[23:]
      print(developer)

      changedTask.developer = developer

      # Получаем ID сообщений
      chat_id = update.callback_query.message.chat_id
      user_message_id = update.callback_query.message.message_id
      bot_message_id = context.user_data.get("bot_message_id")

      # Используем метод processMessage для обработки сообщений
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Исполнитель: {developer}", "TaskInfoForChangeTask")

    #
    # Обработка статусов для команд
    #

    if "chosenProject" in context.user_data:
      team = await getListDevelopersIdByProjectId(context.user_data["chosenProject"])

    if state == "addNewDeveloper":
      # Если нет такого пользователя в списке тимы
      if user_text not in team:
        new_developer = Developer(int(user_text), context.user_data["chosenProject"], "user")
        await addUserToTeam(new_developer.to_dict())
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
        await deleteUserFromTeam(int(user_text), context.user_data["chosenProject"])
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
