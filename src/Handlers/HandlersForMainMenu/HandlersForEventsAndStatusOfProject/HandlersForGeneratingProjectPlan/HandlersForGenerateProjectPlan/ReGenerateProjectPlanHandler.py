from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any
from Handlers.Handler import Handler
import json

from Handlers.RequestsHandler import get_project_re_plan_with_problem

class ReGenerateProjectPlanHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    #problem = context.user_data["problem"]
    if not context.user_data["problem"]:
       problem = ""
    print(f"problem - {problem}")

    loading_message = await query.edit_message_text("🔄 Идет генерация плана, это может занять некоторое время...")

    last_bot_message_id = context.user_data["IdLastMessageFromBot"]
    if update.message:
      chat_id = update.message.chat_id
    else:
      chat_id = update.callback_query.message.chat_id
    if last_bot_message_id:
      try:
        await context.bot.delete_message(chat_id, last_bot_message_id)
      except:
        print(f"Ошибка при удалении последнего сообщения бота")

    keyboard = [
      [InlineKeyboardButton("✅ Принять план", callback_data="saveGeneratedPlan")], # Сохраняем план и уточняем по генерации задач
      [InlineKeyboardButton("✏️ Указать замечания", callback_data="getProblem")],
      [InlineKeyboardButton("🔄 Переделать", callback_data="generateRePlan")],
      [InlineKeyboardButton("❌ Отмена", callback_data="cancelGenerateProjectPlan")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    proj_id = context.user_data["chosenProject"]
    print(f"proj - {proj_id}")

    iam_token = "t1.9euelZqdkZvMj8iWm5mXno2TmJCJju3rnpWanoyPkpnJzs2TmcmUz8fGncvl8_d4PylA-e8kS348_d3z9zhuJkD57yRLfjz9zef1656Vmoyek8zNlZiQjI3Jy4_HlpKR7_zF656Vmoyek8zNlZiQjI3Jy4_HlpKR.qkn44r7OuaM8AL3sNH7hXdjuUk00yaRG4EQoMzlW-hBg-z7El6OTiLYr7vyRWN_6JoehuRBtMZq4TVeG9NiWAg"
    folder_id = "b1gc80aslek1slbmcvj9"

    MAX_MESSAGE_LENGTH = 4096
    resp = await get_project_re_plan_with_problem(problem, proj_id, iam_token, folder_id)

    context.user_data["problem"] = None
    print(f"problem - {context.user_data['problem']}")

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

            #await update.effective_message.reply_markdown(part,reply_markup=reply_markup)
            await query.edit_message_text(part,reply_markup=reply_markup)
    else:
        #await update.effective_message.reply_markdown(plan,reply_markup=reply_markup)
        await query.edit_message_text(plan,reply_markup=reply_markup)
