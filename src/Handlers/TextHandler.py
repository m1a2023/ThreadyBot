from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes

class TextHandler:
  @staticmethod
  async def processMessage(
    context: ContextTypes.DEFAULT_TYPE,
    chat_id: int,
    user_message_id: int,
    bot_message_id: int,
    new_info: str,
    info_key: str
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
      context.user_data[info_key] += new_info

      # Отправляем новое сообщение с обновленной информацией
      last_message_from_bot = await context.bot.send_message(chat_id, context.user_data[info_key])

      # Сохраняем ID нового сообщения бота
      context.user_data["IdLastMessageFromBot"] = last_message_from_bot.message_id

      # Сбрасываем состояние
      context.user_data["state"] = None
      
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    project = context.user_data["project"]
    chat_id = update.message.chat_id
    user_message_id = update.message.message_id
    bot_message_id = context.user_data.get("bot_message_id")

    # Получаем текущее состояние
    state = context.user_data.get("state")

    if state == "setNameForCreateProject":
      project.set_name(user_text)
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"Имя проекта: {user_text}", "projectInfoForCreateProject"
      )

    elif state == "setDescriptionForCreateProject":
      project.set_description(user_text)
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"\nОписание проекта: {user_text}", "projectInfoForCreateProject"
      )

    elif state == "setTeamForCreateProject":
      project.set_team(user_text)
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"\nГруппа разработчиков: {user_text}", "projectInfoForCreateProject"
      )

    elif state == "setLinkForCreateProject":
      project.set_link_rep(user_text)
      await TextHandler.processMessage(
        context, chat_id, user_message_id, bot_message_id,
        f"\nСсылка на репозиторий: {user_text}", "projectInfoForCreateProject"
      )