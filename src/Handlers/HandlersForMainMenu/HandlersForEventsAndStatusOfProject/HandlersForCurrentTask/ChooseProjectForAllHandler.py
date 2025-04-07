from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from Handlers.Handler import Handler
from Handlers.RequestsHandler import getAllProjectsByDevId, getAllProjectsByOwnerId
from ProjectManagment.ProjectManager import ProjectManager


class ChooseProjectForAllHandler(Handler):
    @staticmethod
    async def handle(update, context):
      query = update.callback_query
      await query.answer()

      user_id = update.effective_user.id
      managed_projects = await getAllProjectsByOwnerId(user_id)
      dev_projects = await getAllProjectsByDevId(user_id)

      # Получаем названия проектов
      managed_names = await ProjectManager.get_projects_names_and_id_from_list(managed_projects) if managed_projects else []
      dev_names = await ProjectManager.get_projects_names_and_id_from_list(dev_projects) if dev_projects else []

      # Если нет проектов вообще
      if not managed_names and not dev_names:
          keyboard = [
              [InlineKeyboardButton("🆕 Создать проект", callback_data="CreateProject")],
              [InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")]
          ]
          reply_markup = InlineKeyboardMarkup(keyboard)
          await query.edit_message_text(text="У вас пока нет проектов", reply_markup=reply_markup)
          context.user_data["state"] = None
          return

      keyboard = []
      max_rows = max(len(managed_names), len(dev_names))

      # Добавляем заголовки, если есть хотя бы один проект в колонке
      headers = []
      if managed_names:
          headers.append(InlineKeyboardButton("Управляемые проекты", callback_data="no_action"))
      if dev_names:
          headers.append(InlineKeyboardButton("Пользовательские проекты", callback_data="no_action"))
      if headers:
          keyboard.append(headers)

      # Заполняем строки проектами
      for i in range(max_rows):
          row = []
          if i < len(managed_names):
              row.append(InlineKeyboardButton(managed_names[i][0], callback_data=f"chosenFromAllProjects_{managed_names[i][1]}"))
          elif managed_names:  # Если есть управляемые проекты, но текущей строки нет - добавляем пустую кнопку
              row.append(InlineKeyboardButton(" ", callback_data="no_action"))

          if i < len(dev_names):
              row.append(InlineKeyboardButton(dev_names[i][0], callback_data=f"chosenFromAllProjects_{dev_names[i][1]}"))
          elif dev_names:  # Если есть dev-проекты, но текущей строки нет - добавляем пустую кнопку
              row.append(InlineKeyboardButton(" ", callback_data="no_action"))

          if row:
              keyboard.append(row)

      # Добавляем кнопку Назад
      keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="EventsAndStatusOfProjects")])

      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text(text="Выберите проект", reply_markup=reply_markup)
      context.user_data["state"] = None