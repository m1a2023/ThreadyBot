from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.CurrentTasksHandler import CurrentTasksHandler
from Handlers.RequestsHandler import updateTaskById

class FastEditTaskForChangeDeveloper(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    # тут должны считывать дату и записывать ее в бд

    task_id = context.user_data["taskInCurrentTasks"]
    dev_id = context.user_data["chosenDeveloper"]
    await updateTaskById(task_id, {"user_id": dev_id})
    
    return await CurrentTasksHandler.handle(update, context)
