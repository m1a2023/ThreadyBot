from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

""" Тут предполагается, что в контекст будет подгружаться тима выбранного проекта, тк этого пока нет, 
я напишу это хардкодом, дальше это нужно заменить на запрос """

class ChangeInfoAboutTeamHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    if "team" not in context.user_data:
      # Типа выгрузка из бд (вообще, здесь должны быть имена, но пока id)
      context.user_data["team"] = ["1356189545", "623234185"]

    team = context.user_data["team"]
    team_text = "\n".join(team)

    keyboard = [
        [InlineKeyboardButton("Добавить нового разработчика", callback_data="addNewDeveloper")],
        [InlineKeyboardButton("Удалить разработчика", callback_data="deleteDeveloper")],
        [
          InlineKeyboardButton("Отмена", callback_data="cancelChangeTeam"),
          InlineKeyboardButton("Сохранить", callback_data="saveChangeTeam")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"Изменение команды.\nВаша команда на данный момент:\n{team_text}\nВыберите действие", reply_markup=reply_markup)
