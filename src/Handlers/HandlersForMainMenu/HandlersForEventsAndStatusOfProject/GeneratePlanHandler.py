from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from Handlers.Handler import Handler
from Handlers.RequestsHandler import get_project_plan

import json
class GeneratePlanHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        proj_id = 2 #context.user_data["chosenProject"]

        iam_token = "t1.9euelZqJzZGTj5GKk8uJjZiXjp6Wnu3rnpWanoyPkpnJzs2TmcmUz8fGncvl8_cYO3VA-e8LMm9__d3z91hpckD57wsyb3_9zef1656Vms-Lz8mdl83Ni5iYmImei8aX7_zF656Vms-Lz8mdl83Ni5iYmImei8aX.oTJ4RkqpLLR01-7si8QYo6IbbWaSswacw8_c9sy-VUXJe0XFxOsMW7QiQkvFd9q9SkPJDzgBLMAChj6UVd7rBg"
        folder_id = "b1gc80aslek1slbmcvj9"

        MAX_MESSAGE_LENGTH = 4096  # Максимальная длина сообщения в Telegram

        plan = await get_project_plan(proj_id, iam_token, folder_id)

        # Преобразуем dict в строку (если это словарь)
        if isinstance(plan, dict):
            plan = json.dumps(plan, indent=2, ensure_ascii=False)

        message_length = len(plan)  # Длина всего сообщения

        if message_length > MAX_MESSAGE_LENGTH:
            parts_count = -(-message_length // MAX_MESSAGE_LENGTH)  # Округляем вверх (аналог math.ceil)

            for i in range(parts_count):
                start = i * MAX_MESSAGE_LENGTH
                end = (i + 1) * MAX_MESSAGE_LENGTH
                part = plan[start:end]

                await update.effective_message.reply_text(part)
        else:
            await update.effective_message.reply_text(plan)
