from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getTeamByProjectId, getUserNameById


class SetExecutorForTaskHandler(Handler):
    @staticmethod
    async def handle(update, context):
        query = update.callback_query
        await query.answer()

        chat_id = query.message.chat_id
        context.user_data["state"] = "setExecutorForTask"  # Сохраняем состояние пользователя

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

        sent_message = await query.message.reply_text("Выберите разработчика:", reply_markup = reply_markup)
        context.user_data["bot_message_id"] = sent_message.message_id
