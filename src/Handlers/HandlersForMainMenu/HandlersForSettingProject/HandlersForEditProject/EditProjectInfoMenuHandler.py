from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler

class EditProjectInfoMenuHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        proj_name = context.user_data["project_name"]
        if context.user_data["project_manager"].found_project(proj_name, update, context):
            keyboard = [
                [InlineKeyboardButton("Изменить имя", callback_data="editProjectName")],
                [InlineKeyboardButton("Изменить описание", callback_data="editProjectDescription")],
                [InlineKeyboardButton("Изменить ссылку на репо", callback_data="editProjectLink")],
                [
                    InlineKeyboardButton("Отмена", callback_data="123"),
                    InlineKeyboardButton("Готово", callback_data="saveProjectChanges")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            #вот тут надо адаптировать под метод process message
            sent_message=await update.message.reply_text(f"Вы выбрали для редактирования проект: {proj_name}\nВыберите действие:",reply_markup=reply_markup)
        else:
            sent_message=await update.message.reply_text("Такого проекта нет")
        context.user_data["bot_message_id"] = sent_message.message_id
