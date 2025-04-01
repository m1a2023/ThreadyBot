from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.CurrentTasksHandler import CurrentTasksHandler
from Handlers.RequestsHandler import getTaskById, updateTaskById

class FastEditTaskForChangeDeadlineHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    _, year, month, day = update.callback_query.data.split("_")
    selected_date_str = f"{year}-{month}-{day}"
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d")

    if selected_date < datetime.now():
      return

    task_id = context.user_data["taskInCurrentTasks"]
    await updateTaskById(task_id, {"deadline": selected_date.isoformat()})
    
    return await CurrentTasksHandler.handle(update, context)
