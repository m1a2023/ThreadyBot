from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.CurrentTasksHandler import CurrentTasksHandler
from Handlers.RequestsHandler import updateTaskById

class FastEditTaskForStatusDone(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    task_id = context.user_data["taskInCurrentTasks"]
    await updateTaskById(task_id, {"status": "done"})
    
    return await CurrentTasksHandler.handle(update, context)
