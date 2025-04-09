from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from Handlers.Handler import Handler
from Handlers.RequestsHandler import get_project_plan

import json

class GeneratePlanHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        proj_id = context.user_data["chosenProject"]

        iam_token = "t1.9euelZrNz8iQycaSm86PmpvGicnIzO3rnpWanoyPkpnJzs2TmcmUz8fGncvl8_dRFyxA-e8Tf2tt_t3z9xFGKUD57xN_a23-zef1656VmpnJz5POxpaLyMiZyMiYk53L7_zF656VmpnJz5POxpaLyMiZyMiYk53L._XvvSoGbd9ue_9bwBRXZESvAeUE0P445j1s_khiDZqwL9hxTI46OfmEMONt2rOiUYKq5mY6KlNyCz4q_5RMVBA"
        folder_id = "b1gc80aslek1slbmcvj9"

        MAX_MESSAGE_LENGTH = 4096
        resp = await get_project_plan(proj_id, iam_token, folder_id)
        plan = resp["result"]["alternatives"][0]["message"]["text"]


        if isinstance(plan, dict):
            plan = json.dumps(plan, indent=2, ensure_ascii=False)

        message_length = len(plan)

        if message_length > MAX_MESSAGE_LENGTH:
            parts_count = -(-message_length // MAX_MESSAGE_LENGTH)

            for i in range(parts_count):
                start = i * MAX_MESSAGE_LENGTH
                end = (i + 1) * MAX_MESSAGE_LENGTH
                part = plan[start:end]

                await update.effective_message.reply_markdown(part)
        else:
            await update.effective_message.reply_markdown(plan)
