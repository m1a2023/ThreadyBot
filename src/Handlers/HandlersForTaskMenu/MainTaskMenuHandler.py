from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager

from Handlers.Handler import Handler

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

class MainTaskMenuHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        query = update.callback_query
        await query.answer()

        await TaskManager.get_and_update_list_tasks(update, context, context.user_data["chosenProject"])

        keyboard = [
            [InlineKeyboardButton("🆕 Добавить задачу", callback_data="createNewTask")],
            [InlineKeyboardButton("✏️ Редактировать задачу", callback_data="editTask")],
            [InlineKeyboardButton("🗑️ Удалить задачу", callback_data="confirmationDeleteTask")],
            [InlineKeyboardButton("🔍 Показать задачи", callback_data="showTask")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="SettingsOfProjects")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("*\=\=Редактирование задач\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")
