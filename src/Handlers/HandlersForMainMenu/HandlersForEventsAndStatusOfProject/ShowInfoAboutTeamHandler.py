from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getTeamByProjectId, getUserNameById

class ShowInfoAboutTeamHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:

    query = update.callback_query
    await query.answer()

    context.user_data["team"] = await getTeamByProjectId(context.user_data["chosenProject"])

    team = context.user_data["team"]
    dev_id_list = []
    for dict in team:
      if dict["role"] == "admin":
        owner_id = dict["user_id"]
      else:
        dev_id_list.append(dict["user_id"])
    
    owner_name = await getUserNameById(owner_id)
    owner_link = f'<a href="tg://user?id={owner_id}">{owner_name}</a>'

    dev_name_list = []
    for id in dev_id_list:
      dev_name_list.append(await getUserNameById(id))

    dev_links = []
    for dev_id in dev_id_list:
      dev_name = await getUserNameById(dev_id)
      dev_link = f'<a href="tg://user?id={dev_id}">{dev_name}</a>'
      dev_links.append(f"🔹 {dev_link} - {dev_id}")

    dev_links_text = "\n".join(dev_links)
    if dev_id_list:
      team_text = f"Владелец проекта: {owner_link}\nРазработчики проекта:\n{dev_links_text}"
    else:
      team_text = f"Владелец проекта: {owner_link}"
    keyboard = [
        [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"<b>==Просмотр команды==</b>\n{team_text}", reply_markup=reply_markup, parse_mode="HTML")
