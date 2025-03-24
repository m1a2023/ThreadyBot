from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any


from LLMgen.GeneratePlan import generateProjectPlan
from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForGeneratingProjectPlan.GeneratingProjectPlanMenuHandler import GeneratingPlanMenuHandler
from Handlers.RequestsHandler import getProjectById
from ProjectManagment.ProjectManager import ProjectManager

from LLMgen.GeneratePlan import generateProjectPlan


class ShowCurrentPlanHandler(Handler):

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()

        keyboard = [
            [InlineKeyboardButton("Назад", callback_data="generate_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await query.edit_message_text(f"Текущий план: \n{context.user_data['current_plan']}", reply_markup=reply_markup)

        except:
            await query.edit_message_text(f"Текущего плана нет", reply_markup=reply_markup)