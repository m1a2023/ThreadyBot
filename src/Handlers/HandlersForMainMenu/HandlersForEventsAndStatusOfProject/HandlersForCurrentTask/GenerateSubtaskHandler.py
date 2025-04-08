from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any
from Handlers.Handler import Handler


class GenerateSubtaskHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    task_id = context.user_data["taskInCurrentTasks"]
    # await getTaskById(task_id) - для получения инфы о задаче (еще нужен будет импорт) Удалить комментарий, если не нужно

    # Где-то здесь начинается генерация подтасков
    
    subtaskText = "текст подзадач"
    
    await query.edit_message_text("🔄 Идет генерация, это может занять некоторое время...")
    
    keyboard = [
      [InlineKeyboardButton("😊 Спасибо", callback_data="EventsAndStatusOfProjects")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(f"{subtaskText}", reply_markup=reply_markup)