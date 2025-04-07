from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForCurrentTask.CreateKeyboardForCurrentTasks import CreateKeyboardForCurrentTasks
from TaskManagement.TaskManager import TaskManager

class CurrentTasksHandler(Handler): 
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    query = update.callback_query
    await query.answer()

    await TaskManager.get_and_update_list_tasks(update, context, context.user_data["chosenProject"])

    # [{'title': 'task1', 
    # 'deadline': '2025-03-31T00:00:00', 
    # 'user_id': 1356189545, 
    # 'created_at': '2025-03-24T14:08:52.910076', 
    # 'changed_at': '2025-03-24T14:09:41.976852', 
    # 'description': '1234', 
    # 'priority': 'high', 
    # 'status': 'done', 
    # 'project_id': 1, 'id': 1}
   
    all_tasks = context.user_data["task_manager"].tasks
    if all_tasks == []:
      keyboard = [
        [InlineKeyboardButton(f"🆕 Создать задачу", callback_data="createNewTask")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")]
      ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text(text="Нет задач по выбранному проекту", reply_markup=reply_markup)
    
    else:
      todo_tasks = [] # Таски со статусом todo
      in_progress_tasks = [] # Таски со статусом "в процессе"
      for task in all_tasks:
        if task["status"] == "todo":
          todo_tasks.append(task)
        elif task["status"] == "in_progress":
          in_progress_tasks.append(task)
      
      keyboard = await CreateKeyboardForCurrentTasks.create_tasks_keyboard(todo_tasks, in_progress_tasks)
      keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")])
      reply_markup = InlineKeyboardMarkup(keyboard)

      await query.edit_message_text("Выберите задачу для просмотра информации:", reply_markup=reply_markup)