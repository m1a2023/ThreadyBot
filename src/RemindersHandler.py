from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

import asyncio
import httpx
import datetime
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone, timedelta

from Handlers.Handler import Handler
from Handlers.RequestsHandler import get_all_tasks_deadlines

class RemindersHandler(Handler):
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        tasks = await get_all_tasks_deadlines()
        for task in tasks:
            if (task[1] - datetime.now(timezone.utc)).total_seconds() / 3600 <= 24 and task[3]: # task[3] - это маркер отправлено/неотправлено напоминнаине
                if task[2]: # task[2] - это id разраба
                    RemindersHandler.fetch_and_send_reminders(task[0])
                else:
                    pass # нужно придумать как разослать всем разрабам проекта напоминание о дедлайне

    @staticmethod
    async def fetch_and_send_reminders(update: Update, context: ContextTypes.DEFAULT_TYPE, task_title: str = None):
        if task_title:

            message = (
                f"🔔 *Напоминание!*\n"
                f"Задача: *{task_title}* ⏳\n"
                f"Осталось менее 24 часов до дедлайна!"
            )

            try:
                await context.bot.send_message(text=message, parse_mode="Markdown")

                # Отмечаем в БД, что уведомление отправлено (нужно реализовать `mark_task_reminder_sent`)
                #await mark_task_reminder_sent(task_id)
            except Exception as e:
                print(f"Ошибка при отправке напоминания: {e}")
        else:
            pass
