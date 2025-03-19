from urllib.parse import urlparse
from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from Handlers.HandlersForMainMenu.HandlersForSettingProject.HandlersForEditProject.EditProjectInfoMenuHandler import EditProjectInfoMenuHandler
from Handlers.HandlersForTaskMenu.EditTaskMenu.EditTaskMenuHandler import EditTaskMenuHandler
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


    if state == "deleteProject":
      await update.message.reply_text(await context.user_data["project_manager"].delete_project(user_text, update, context))
      del context.user_data["task_manager"]
      """await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"{user_text}", "projectInfoForDeleteProject"
        )"""

    elif state == "editProjectName":
      context.user_data["project_manager"].found_project(context.user_data["project_name"],update,context).set_name(user_text)
      context.user_data["project_name"] = user_text

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Имя проекта: {user_text}", "projectInfoForEditProject"
        )
    elif state == "editProjectDescription":
      context.user_data["project_manager"].found_project(context.user_data["project_name"],update,context).set_description(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Описание проекта: {user_text}", "projectInfoForEditProject"
        )
    elif state == "editProjectDeadline":
      context.user_data["project_manager"].found_project(context.user_data["project_name"],update,context).set_deadline(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Дедлайн проекта: {user_text}", "projectInfoForEditProject"
        )
    elif state == "editProjectLink":
      context.user_data["project_manager"].found_project(context.user_data["project_name"],update,context).set_link_rep(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Ссылка на репозиторий проекта: {user_text}", "projectInfoForEditProject"
        )
    elif state == "editProjectTeam":
      context.user_data["project_manager"].found_project(context.user_data["project_name"],update,context).set_team(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Дедлайн проекта: {user_text}", "projectInfoForEditProject"
        )

    elif state == "editProject":
      context.user_data["project_name"] = user_text
      return await EditProjectInfoMenuHandler.handle(update,context)


    elif state == "setNameForCreateProject":
      # Требования к названию проекта: длина названия не менее 4 символов и не должно начинаться с цифры
      # Если ввод корректен, обновляем информацию
      if (len(user_text) >= 4 and not user_text[0].isdigit()):
        project.set_name(user_text)
        await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Имя проекта: {user_text}", "projectInfoForCreateProject"
        )

        # Сохраняем имя/юзернейм пользователя как владельца проекта
        if update.message.from_user.username:
          project.set_id_owner("@" + update.message.from_user.username)
        else:
          project.set_id_owner(update.message.from_user.full_name)

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
      context.user_data["task_name"] = user_text
      return await EditTaskMenuHandler.handle(update, context)
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
