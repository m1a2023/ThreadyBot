from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from Handlers.Handler import Handler
from Handlers.RequestsHandler import get_project_plan

import json
class GeneratePlanHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        proj_id = context.user_data["chosenProject"]

        iam_token = ""
        folder_id = ""

        MAX_MESSAGE_LENGTH = 4096
        plan = await get_project_plan(proj_id, iam_token, folder_id)

        if isinstance(plan, dict):
            plan = json.dumps(plan, indent=2, ensure_ascii=False)

        message_length = len(plan)

        if message_length > MAX_MESSAGE_LENGTH:
            parts_count = -(-message_length // MAX_MESSAGE_LENGTH)

            for i in range(parts_count):
                start = i * MAX_MESSAGE_LENGTH
                end = (i + 1) * MAX_MESSAGE_LENGTH
                part = plan[start:end]

                await update.effective_message.reply_text(part)
        else:
            await update.effective_message.reply_text(plan)
