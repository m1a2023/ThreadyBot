from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from ProjectManagment.Project import Project
from ProjectManagment.ProjectManager import ProjectManager

class EditProjectInfoHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        await ProjectManager.get_and_update_list_projects(update, context)

        if "changedProject" not in context.user_data:
            context.user_data["changedProject"] = Project()
            context.user_data["projectInfoForChangeProject"] = ["Вы ввели:"]

        keyboard = [
            [InlineKeyboardButton("✏️ Изменить название", callback_data="changeNameProject")],
            [InlineKeyboardButton("✏️ Изменить описание", callback_data="changeDescriptionProject")],
            [InlineKeyboardButton("📎 Изменить ссылку на репозиторий", callback_data="changeLinkProject")],
            [
                InlineKeyboardButton("❌ Отмена", callback_data="cancelProjectEdit"),
                InlineKeyboardButton("✅ Сохранить", callback_data="saveProjectChanges")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("*\=\=Изменение данных проекта\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")