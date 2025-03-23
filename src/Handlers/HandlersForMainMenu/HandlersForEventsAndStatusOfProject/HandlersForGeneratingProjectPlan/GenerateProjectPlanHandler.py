from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


from src.LLMgen.GaneratePlan import GaneratePlan
from src.ProjectManagment.ProjectManager import ProjectManager
from Handlers.Handler import Handler

class GenerateProjectPlanHandler(Handler):
  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

""" Это всё ниже буду переписывать
    try:
      await context.user_data["project_manager"].show_projects(update, context)
      list_projects = await context.user_data["project_manager"].get_projects_list(update, context)

      keyboard = [ [InlineKeyboardButton('Назад', callback_data='generatePlanMenu')]]
      reply_markup = InlineKeyboardMarkup(keyboard)
      user_index = int(await query.message.reply_text("Введите номер проекта:"))
      user_project = None
      for index, project in list_projects:
        if index == user_index:
          user_project = project

      if user_project:
        await update.message.reply_text("Несуществующий проект", reply_markup=reply_markup)

      plan = GaneratePlan(user_project)
      await query.edit_message_text(f"Новый план: {plan}", reply_markup=reply_markup)





    except:
      keyboard = [ [InlineKeyboardButton(f"Назад", callback_data="generatePlanMenu")]  ]
      reply_markup = InlineKeyboardMarkup(keyboard)
      await query.edit_message_text(f"Список проектов пуст ", reply_markup=reply_markup)




    #plan = GaneratePlan(ContextTypes.user_data)

    #await query.edit_message_text(f"Новый план: {plan}", reply_markup=reply_markup)
 """