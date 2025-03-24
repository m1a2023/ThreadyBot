from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any


from src.LLMgen.GeneratePlan import generateProjectPlan
from Handlers.Handler import Handler
from Handlers.HandlersForMainMenu.HandlersForEventsAndStatusOfProject.HandlersForGeneratingProjectPlan.GeneratingProjectPlanMenuHandler import GeneratingPlanMenuHandler
from Handlers.RequestsHandler import getProjectById
from ProjectManagment.ProjectManager import ProjectManager

from src.LLMgen.GeneratePlan import generateProjectPlan


class SaveGeneratedPlanHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):

        context.user_data['current_plan'] = context.user_data['temp_plan']
        context.user_data['temp_plan'] = None

        return await GeneratingPlanMenuHandler.handle(update, context)