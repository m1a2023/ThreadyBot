from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getProjectInfoById, getUserNameById
from Handlers.MainMenuHandler import MainMenuHandler


class ShowChatLinkHandler(Handler):
    @staticmethod
    async def handle(update, context):

      query = update.callback_query
      await query.answer()

      project_id= context.user_data["chosenProject"] 
      project = await getProjectInfoById(project_id)
      if project["chat_link"] is not None:
        owner_id = project["owner_id"]
        owner_name = await getUserNameById(owner_id)
        owner_link = f'<a href="tg://user?id={owner_id}">{owner_name}</a>'

        message = f"Ссылка на общий чат проекта {project['title']} (Создатель: {owner_link}):\n{project['chat_link']}"
        await context.bot.delete_message(chat_id=update.callback_query.message.chat_id, message_id=update.callback_query.message.message_id)
        await query.message.reply_text(message, parse_mode="HTML", disable_web_page_preview=True)
        return await MainMenuHandler.handle(update, context)
      else:
        keyboard =[
          [InlineKeyboardButton("⬅️ Назад", callback_data="MoveToMainMenu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("У выбранного проекта нет ссылки на общий чат", reply_markup=reply_markup)
