from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any
from Handlers.Handler import Handler


class GenerateProjectPlanHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    project_id = context.user_data["chosenProject"]
    # await getAllTasks(project_id) - для получения всех задач по проекту (еще нужен будет импорт) Удалить комментарий, если не нужно

    # Где-то здесь начинается генерация плана
    
    planText = "текст плана"
    
    await query.edit_message_text("🔄 Идет генерация плана, это может занять некоторое время...")
    
    keyboard = [
      [InlineKeyboardButton("✅ Принять план", callback_data="saveGeneratedPlan")], # Сохраняем план и уточняем по генерации задач
      [InlineKeyboardButton("🔄 Переделать", callback_data="generateNewPlan")], # По-идее, этот же хендлер просто перезапуститься
      [InlineKeyboardButton("❌ Отмена", callback_data="cancelGenerateProjectPlan")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"{planText}", reply_markup=reply_markup)