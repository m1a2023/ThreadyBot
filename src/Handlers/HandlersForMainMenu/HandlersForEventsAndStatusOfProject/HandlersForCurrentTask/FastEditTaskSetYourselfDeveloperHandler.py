from typing import Any

from Handlers.Handler import Handler
from Handlers.RequestsHandler import updateTaskById
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.CurrentTasksHandler import CurrentTasksHandler


class FastEditTaskSetYourselfDeveloper(Handler):
    @staticmethod
    async def handle(update, context):
      query = update.callback_query
      await query.answer()

      user_id = update.effective_user.id
      await updateTaskById(context.user_data["taskInCurrentTasks"], {"user_id": user_id})

      return await CurrentTasksHandler.handle(update, context)