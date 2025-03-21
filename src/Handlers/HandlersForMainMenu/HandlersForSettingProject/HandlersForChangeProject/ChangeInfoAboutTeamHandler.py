from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getTeamByProjectId, getUserNameById

class ChangeInfoAboutTeamHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    context.user_data["team"] = await getTeamByProjectId(context.user_data["chosenProject"])

    # [{'role': 'admin', 'project_id': 27, 'created_at': '2025-03-21T23:41:15.849326', 'user_id': 8028994392, 'id': 10}, 
    #  {'role': 'user', 'project_id': 27, 'created_at': '2025-03-21T23:41:16.361557', 'user_id': 1356189545, 'id': 11}]
    team = context.user_data["team"]
    dev_id_list = []
    for dict in team:
      if dict["role"] == "admin":
        owner_id = dict["user_id"]
      else:
        dev_id_list.append(dict["user_id"])
    
    owner_name = await getUserNameById(owner_id)
    dev_name_list = []
    for id in dev_id_list:
      dev_name_list.append(await getUserNameById(id))
    
    dev_data = []
    for i in range(0, len(dev_id_list)):
      dev_data.append(f"{dev_name_list[i]} - {dev_id_list[i]}")
    
    dev_name_and_id = "\n".join(dev_data)

    team_text = f"Владелец проекта:\n{owner_name} - {owner_id}\nРазработчики проекта:\n{dev_name_and_id}"

    keyboard = [
        [InlineKeyboardButton("Добавить нового разработчика", callback_data="addNewDeveloper")],
        [InlineKeyboardButton("Удалить разработчика", callback_data="deleteDeveloper")],
        [
          InlineKeyboardButton("Отмена", callback_data="cancelChangeTeam"),
          InlineKeyboardButton("Сохранить", callback_data="saveChangeTeam")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"Изменение команды.\n\nВаша команда на данный момент:\n\n{team_text}\n\n\nВыберите действие", reply_markup=reply_markup)
