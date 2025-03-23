from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getTeamByProjectId, getUserNameById


class ChooseExecutorHandler(Handler):
  @staticmethod
  async def handle(update, context):

    query = update.callback_query
    await query.answer()

    team = await getTeamByProjectId(context.user_data["chosenProject"])

    keyboard = []
    developers_id_and_name = [] #Имена и id разработчиков
    for dict in team:
      id = dict["user_id"]
      name = await getUserNameById(id)
      developers_id_and_name.append((name, id))
    
    # Создаем кнопки
    for dev in developers_id_and_name:
      keyboard.append([InlineKeyboardButton(f"{dev[0]}", callback_data=f"chosenExecuter_{dev[1]}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Выберите разработчика: ", reply_markup=reply_markup)
