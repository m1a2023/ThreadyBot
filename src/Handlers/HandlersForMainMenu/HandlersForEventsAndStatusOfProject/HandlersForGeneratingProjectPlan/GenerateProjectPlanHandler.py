from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any

from LLMgen.GeneratePlan import generateProjectPlan
from Handlers.Handler import Handler
from Handlers.RequestsHandler import getProjectById
from ProjectManagment.ProjectManager import ProjectManager

from LLMgen.GeneratePlan import generateProjectPlan


class GenerateProjectPlanHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    await ProjectManager.get_and_update_list_projects(update, context)

    await query.edit_message_text(f'Подождите идет генерация...')

    chosenProj = context.user_data["chosenProject"]

    foundProject = await getProjectById(int(chosenProj))

    keyboard = [
      [InlineKeyboardButton("Назад", callback_data="generate_menu")],
      [InlineKeyboardButton('Сохранить этот план', callback_data='save_generated_plan')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    plan = await generateProjectPlan(foundProject)

    context.user_data['temp_plan'] = plan

    await query.edit_message_text(f"Данные о проекте:\n{foundProject.__str__()}\n\nПлан:\n{plan}", reply_markup=reply_markup)

    context.user_data["chosenProject"] = None
