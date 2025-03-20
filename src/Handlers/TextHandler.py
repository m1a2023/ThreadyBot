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
      await update.message.reply_text(await context.user_data["project_manager"].delete_project(user_text, update, context))\

      project_name = context.user_data["project_name"]
      if project_name in context.user_data["task_managers"]:
        del context.user_data["task_managers"][project_name]

      """await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"{user_text}", "projectInfoForDeleteProject"
        )"""

    elif state == "chooseProject":
       #тут будет запрос к бд
       print(user_text)
       if context.user_data["project_manager"].found_project(user_text, update, context):
          return await ChangeProjectHandler.handle(update, context)
       else:
          await update.message.reply_text("Такого проекта нет")

    elif state == "editProjectName":
        try:
            # Название проекта должно содержать только буквы, цифры и пробелы
            project_name = re.sub(r"[^\w\s]", "", user_text).strip()

            if len(project_name) < 3:
                raise ValueError("Название проекта должно быть не короче 3 символов.")

            context.user_data["project_manager"].found_project(context.user_data["project_name"], update, context).set_name(project_name)
            context.user_data["project_name"] = project_name

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Имя проекта обновлено: {project_name}", "projectInfoForEditProject"
            )
        except ValueError as e:
            error_message = str(e) if str(e) else "Ошибка! Введите корректное название проекта (не менее 3 символов)."
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text=error_message + " Попробуйте снова:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return

    elif state == "editProjectDescription":
        try:
            # Описание проекта не должно быть короче 4 слов
            description = re.sub(r"[^\w\s]", "", user_text).split()

            if len(description) < 4:
                raise ValueError("Описание проекта должно содержать не менее 4 слов.")

            context.user_data["project_manager"].found_project(context.user_data["project_name"], update, context).set_description(user_text)

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Описание проекта обновлено: {user_text}", "projectInfoForEditProject"
            )
        except ValueError as e:
            error_message = str(e) if str(e) else "Ошибка! Введите более детальное описание (не менее 4 слов)."
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text=error_message + " Попробуйте снова:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return

    elif state == "editProjectLink":
        try:
            # Проверяем, является ли введенная строка валидной ссылкой
            regex = r"^(https?://)?(www\.)?[\w.-]+\.\w{2,}(/[\w.-]*)*/?$"
            if not re.match(regex, user_text):
                raise ValueError("Введите корректную ссылку на репозиторий.")

            context.user_data["project_manager"].found_project(context.user_data["project_name"], update, context).set_link_rep(user_text)

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Ссылка на репозиторий обновлена: {user_text}", "projectInfoForEditProject"
            )
        except ValueError as e:
            error_message = str(e) if str(e) else "Ошибка! Введите корректную ссылку на репозиторий."
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text=error_message + " Попробуйте снова:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return

        """elif state == "editProjectTeam":
      context.user_data["project_manager"].found_project(context.user_data["project_name"],update,context).set_team(user_text)

      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"Команда проекта: {user_text}", "projectInfoForEditProject"
        )"""

    elif state == "editProject":

      return await EditProjectInfoMenuHandler.handle(update,context)


    elif state == "setNameForCreateProject":
      # Требования к названию проекта: длина названия не менее 4 символов и не должно начинаться с цифры
      # Если ввод корректен, обновляем информацию
      if (len(user_text) >= 4 and not user_text[0].isdigit()):
        context.user_data["project_name"] = user_text
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
      if len(description) >= 15:
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
      try:
          # Проверяем формат даты
          task_deadline = datetime.strptime(user_text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
          task.set_deadline(user_text)

          await TextHandler.processMessage(
              context, chat_id, user_message_id, bot_message_id,
              f"Дедлайн задачи установлен: {user_text}", "taskInfoForCreateTask"
          )
      except ValueError:
          # Ошибка формата даты
          if bot_message_id:
              try:
                  await context.bot.edit_message_text(
                      chat_id=chat_id,
                      message_id=bot_message_id,
                      text="Ошибка! Введите дату в формате YYYY-MM-DD. Попробуйте еще раз:"
                  )
              except Exception as e:
                  print(f"Ошибка при редактировании сообщения: {e}")
          try:
              await context.bot.delete_message(chat_id, user_message_id)
          except Exception as e:
              print(f"Ошибка при удалении сообщения пользователя: {e}")
          return

    elif state == "setPriorityForTask":
        try:
            # Проверяем приоритет
            valid_priorities = ["low", "medium", "high"]
            if user_text.lower() not in valid_priorities:
                raise ValueError

            task.set_priority(user_text)

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Приоритет задачи установлен: {user_text}", "taskInfoForCreateTask"
            )
        except ValueError:
            # Ошибка ввода приоритета
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text="Ошибка! Приоритет должен быть 'low', 'medium' или 'high'. Попробуйте еще раз:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return

    elif state == "setStatusForTask":
        try:
            # Проверяем статус
            valid_statuses = ["todo", "in progress", "done"]
            if user_text.lower() not in valid_statuses:
                raise ValueError

            task.set_status(user_text)

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Статус задачи установлен: {user_text}", "taskInfoForCreateTask"
            )
        except ValueError:
            # Ошибка ввода статуса
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text="Ошибка! Статус должен быть 'todo', 'in progress' или 'done'. Попробуйте еще раз:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return


    elif state == "deleteTask":
      await context.user_data["task_manager"].delete_task(user_text, update, context)
      await TextHandler.processMessage(
          context, chat_id, user_message_id, bot_message_id,
          f"{user_text}", "taskInfoForDeleteTask"
        )

    elif state == "editTask":
      context.user_data["task_name"] = user_text
      return await EditTaskMenuHandler.handle(update, context)


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
        try:
            # Проверяем формат даты
            task_deadline = datetime.strptime(user_text, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            context.user_data["task_manager"].found_task(context.user_data["task_name"], update, context).set_deadline(user_text)

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Дедлайн задачи обновлен: {user_text}", "taskInfoForEditTask"
            )
        except ValueError:
            # Ошибка формата даты
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text="Ошибка! Введите дату в формате YYYY-MM-DD. Попробуйте еще раз:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return

    elif state == "editTaskPriority":
        try:
            # Проверяем приоритет
            valid_priorities = ["low", "medium", "high"]
            if user_text.lower() not in valid_priorities:
                raise ValueError

            context.user_data["task_manager"].found_task(context.user_data["task_name"], update, context).set_priority(user_text)

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Приоритет задачи обновлен: {user_text}", "taskInfoForEditTask"
            )
        except ValueError:
            # Ошибка ввода приоритета
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text="Ошибка! Приоритет должен быть 'low', 'medium' или 'high'. Попробуйте еще раз:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return

    elif state == "editTaskStatus":
        try:
            # Проверяем статус
            valid_statuses = ["todo", "in progress", "done"]
            if user_text.lower() not in valid_statuses:
                raise ValueError

            context.user_data["task_manager"].found_task(context.user_data["task_name"], update, context).set_status(user_text)

            await TextHandler.processMessage(
                context, chat_id, user_message_id, bot_message_id,
                f"Статус задачи обновлен: {user_text}", "taskInfoForEditTask"
            )
        except ValueError:
            # Ошибка ввода статуса
            if bot_message_id:
                try:
                    await context.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=bot_message_id,
                        text="Ошибка! Статус должен быть 'todo', 'in progress' или 'done'. Попробуйте еще раз:"
                    )
                except Exception as e:
                    print(f"Ошибка при редактировании сообщения: {e}")
            try:
                await context.bot.delete_message(chat_id, user_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения пользователя: {e}")
            return
