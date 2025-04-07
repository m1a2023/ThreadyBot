from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from TaskManagement.Task import Task
from TaskManagement.TaskManager import TaskManager

class EditTaskMenuHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        await TaskManager.get_and_update_list_tasks(update, context, context.user_data["chosenProject"])

        if "changedProject" not in context.user_data:
            context.user_data["changedTask"] = Task()
            context.user_data["TaskInfoForChangeTask"] = ["Вы ввели:"]
        
        keyboard = [
            [InlineKeyboardButton("🏷️ Изменить название", callback_data="editTaskName")],
            [InlineKeyboardButton("📝 Изменить описание", callback_data="editTaskDescription")],
            [InlineKeyboardButton("📅 Изменить дедлайн", callback_data="editTaskDeadline")],
            [InlineKeyboardButton("🚥 Изменить приоритет", callback_data="editTaskPriority")],
            [InlineKeyboardButton("❕ Изменить статус", callback_data="editTaskStatus")],
            [InlineKeyboardButton("🧑‍💻 Изменить исполнителя", callback_data="editTaskDeveloper")],
            [
                InlineKeyboardButton("❌ Отмена", callback_data="cancelEditTask"),
                InlineKeyboardButton("✅ Сохранить", callback_data="saveEditTask")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("*\=\=Изменение данных задачи\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")