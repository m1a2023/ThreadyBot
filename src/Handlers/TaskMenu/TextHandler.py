from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from TaskManagement.TaskManager import TaskManager

class TextHandler(Handler):
    USER_STATE = {}  # Сохраняем выбранную опцию

    name = None
    description = None
    deadline = None
    priority = None
    status = None

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        chat_id = update.message.chat_id
        user_text = update.message.text

        if chat_id in TextHandler.USER_STATE:
            selected_option = TextHandler.USER_STATE[chat_id]  # Какая опция выбрана

            await TextHandler.options(selected_option,user_text,update,context)
            TextHandler.add_data(user_text,selected_option)

            del TextHandler.USER_STATE[chat_id] # Сбрасываем состояние пользователя

    def data_clear():
        print("from dataclear")
        TextHandler.name = None
        TextHandler.description = None
        TextHandler.deadline = None
        TextHandler.priority = None
        TextHandler.status = None

    @staticmethod
    def add_data(data, option):
        print(f"from text handler\n{data,option}")
        if option == "add_name":
            TextHandler.name = data
        elif option == "add_description":
            TextHandler.description = data
        elif option == "add_deadline":
            TextHandler.deadline = data
        elif option == "add_priority":
            TextHandler.priority = data
        elif option == "add_status":
            TextHandler.status = data


    #надо подумать как назвать метод
    #data = user_text
    @staticmethod
    async def options(option, data, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
        print("from option")
        if option == "edit_opt":
            print("from edit option")
            keyboard = [
                [InlineKeyboardButton("Изменить имя", callback_data="edit_name")],
                [InlineKeyboardButton("Изменить описание", callback_data="edit_description")],
                [InlineKeyboardButton("Изменить дедлайн", callback_data="edit_deadline")],
                [InlineKeyboardButton("Изменить приоритет", callback_data="edit_priority")],
                [InlineKeyboardButton("Изменить статус", callback_data="edit_status")],
                [
                    InlineKeyboardButton("Отмена", callback_data="cancel"),
                    InlineKeyboardButton("Готово", callback_data="done")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(f"Вы выбрали для редактирования задачу: {data}\n Выберите действие:",reply_markup=reply_markup)
        elif option == "delete_opt":
            response_text = await TaskManager.delete_task(data, update, context)

            await update.message.reply_text(response_text)
