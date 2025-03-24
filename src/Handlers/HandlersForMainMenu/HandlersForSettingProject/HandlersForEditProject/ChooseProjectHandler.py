from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import getAllProjects
from ProjectManagment.ProjectManager import ProjectManager


class ChooseProjectHandler(Handler):
    @staticmethod
    async def handle(update, context):

        query = update.callback_query
        await query.answer()

        # Обновляем данные о проектах пользователя
        await ProjectManager.get_and_update_list_projects(update, context)
        if context.user_data["project_manager"].projects == []:
            keyboard = [
                [InlineKeyboardButton(f"Создать проект", callback_data="CreateProject")],
                [InlineKeyboardButton("Назад", callback_data="SettingsOfProjects")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text="Ваш список проектов пустой", reply_markup=reply_markup)
            context.user_data["state"] = None
        else:
            keyboard = []
            # Собираем кнопки с проектами
            projects = await context.user_data["project_manager"].get_projects_names_and_id()
            for project in projects:
                keyboard.append([InlineKeyboardButton(f"{project[0]}", callback_data=f"chosenProject_{project[1]}")])
            keyboard.append([InlineKeyboardButton("Назад", callback_data="SettingsOfProjects")])

            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text="Выберите проект: ", reply_markup=reply_markup)
