from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler

from ProjectManagment.ProjectManager import ProjectManager

class MainMenuHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await ProjectManager.get_and_update_list_projects(update, context)

    keyboard = [
      [InlineKeyboardButton("✏️ Настройка проектов", callback_data="SettingsOfProjects")],
      [InlineKeyboardButton("🔍 Cостояние проекта", callback_data="EventsAndStatusOfProjects")],
      [InlineKeyboardButton("⚙️ Общие настройки", callback_data="GeneralSettings")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.callback_query:
      try:
        query = update.callback_query
        await query.answer()  # Подтверждаем callback

        # Редактируем сообщение с кнопками
        await query.edit_message_text(text="*\=\=Главное меню\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")
      except:
        await context.bot.sendMessage(update.effective_chat.id, text="*\=\=Главное меню\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")
    else:
      # Отправляем новое сообщение с кнопками
      await update.message.reply_text(text="*\=\=Главное меню\=\=*\nВыберите действие:", reply_markup=reply_markup, parse_mode="MarkdownV2")
