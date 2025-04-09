from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import Any
from Handlers.Handler import Handler
import json

from Handlers.RequestsHandler import div_task, getTaskById

class GenerateSubtaskHandler(Handler):

  @staticmethod
  async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    query = update.callback_query
    await query.answer()

    await query.edit_message_text("🔄 Идет генерация, это может занять некоторое время...")

    keyboard = [
      [InlineKeyboardButton("😊 Спасибо", callback_data="EventsAndStatusOfProjects")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    task_id = context.user_data["taskInCurrentTasks"]
    task = await getTaskById(task_id) #- для получения инфы о задаче (еще нужен будет импорт) Удалить комментарий, если не нужно
    problem = task.description

    proj_id = context.user_data["chosenProject"]

    iam_token = "t1.9euelZqdkZvMj8iWm5mXno2TmJCJju3rnpWanoyPkpnJzs2TmcmUz8fGncvl8_d4PylA-e8kS348_d3z9zhuJkD57yRLfjz9zef1656Vmoyek8zNlZiQjI3Jy4_HlpKR7_zF656Vmoyek8zNlZiQjI3Jy4_HlpKR.qkn44r7OuaM8AL3sNH7hXdjuUk00yaRG4EQoMzlW-hBg-z7El6OTiLYr7vyRWN_6JoehuRBtMZq4TVeG9NiWAg"
    folder_id = "b1gc80aslek1slbmcvj9"

    MAX_MESSAGE_LENGTH = 4096
    resp = await div_task(proj_id, problem, iam_token, folder_id)
    raw_plan = resp["result"]["alternatives"][0]["message"]["text"]
    plan = format_task_plan(raw_plan)


    message_length = len(plan)

    if message_length > MAX_MESSAGE_LENGTH:
        parts_count = -(-message_length // MAX_MESSAGE_LENGTH)

        for i in range(parts_count):
            start = i * MAX_MESSAGE_LENGTH
            end = (i + 1) * MAX_MESSAGE_LENGTH
            part = plan[start:end]

            await query.edit_message_text(part,reply_markup=reply_markup)
    else:
        await query.edit_message_text(plan,reply_markup=reply_markup)


import re
import json

def format_task_plan(plan_text: str) -> str:
    try:
        plan_json = json.loads(plan_text)
        tasks = plan_json.get("tasks", [])
        formatted_tasks = []

        # Вытаскиваем задачи
        for item in tasks:
            for key, value in item.items():
                value = restore_markdown_links(value)
                formatted_tasks.append(f"📌 Task {key}: {value}")

        # Ищем приоритизацию (оставляем оригинал со ссылками)
        if "Приоритизация задач" in plan_text:
            parts = plan_text.split("Приоритизация задач")
            if len(parts) > 1:
                prioritization = "🧩 Приоритизация задач:\n" + parts[1].strip()
                prioritization = restore_markdown_links(prioritization)
                formatted_tasks.append("\n" + prioritization)
        else:
            auto_priority = "\n🧩 Автоматическая приоритизация задач:\n"
            auto_priority += "\n".join([
                f"Задача {i+1} должна быть выполнена после задачи {i}."
                if i > 0 else f"Задача {i+1} должна быть выполнена первой."
                for i in range(len(tasks))
            ])
            formatted_tasks.append(auto_priority)

        return "\n\n".join(formatted_tasks)

    except Exception as e:
        return f"⚠️ Ошибка форматирования плана: {e}"


def restore_markdown_links(text: str) -> str:
    # Исправляем ссылки, если они заданы явно как [text](url)
    # Иногда парсеры заменяют их на текстовые ссылки "text: url"
    text = re.sub(r'([^\s\]]+):\s+(https?://\S+)', r'[\1](\2)', text)
    return text
