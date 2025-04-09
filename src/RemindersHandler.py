from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from typing import List

import asyncio
import httpx
import datetime
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timezone, timedelta

from Handlers.Handler import Handler
from ProjectManagment.ProjectManager import ProjectManager
from Handlers.RequestsHandler import get_reminders_by_project_ids, getTeamByProjectId, delete_remind_by_task_id

class RemindersHandler(Handler):
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await ProjectManager.get_and_update_list_projects(update, context)

        project_ids = []

        projects = context.user_data["project_manager"].projects
        for project in projects:
            project_ids.append(project["id"])
        print(project_ids)

        tasks = await get_reminders_by_project_ids(project_ids)

        if tasks is None:
            return

        print(tasks)
        for task in tasks:
            reminder_time = datetime.fromisoformat(task[1]).replace(tzinfo=timezone.utc)

            print(reminder_time, datetime.now(timezone.utc))

            if (reminder_time <= datetime.now(timezone.utc)):
                print(f"условие выполнилось. Проект - {task[3]}. Задача - {task[0]}")
                if task[2]: # task[2] - это id разраба
                    await RemindersHandler.fetch_and_send_reminders(context, task[0], task[2], task[4])
                else:
                    proj_id = task[3]
                    teams = await getTeamByProjectId(proj_id)

                    for team in teams:
                        await RemindersHandler.fetch_and_send_reminders(context, task[0], team['user_id'], task[4])
            else:
                print(f"условие не выполнилось. Проект - {task[3]}. Задача - {task[0]}")

    @staticmethod
    async def fetch_and_send_reminders(context: ContextTypes.DEFAULT_TYPE, task_title: str, user_id: int, task_id: int):
        keyboard = [
            [InlineKeyboardButton("Ок", callback_data="OK_reminder")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        print("send")
        if task_title:

            message = (
                f"🔔 *Напоминание!*\n"
                f"Задача: *{task_title}* ⏳\n"
                f"Осталось менее 24 часов до дедлайна!"
            )

            try:
                sent_message = await context.bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown", reply_markup=reply_markup)
                context.user_data["bot_message_id"] = sent_message.message_id
                # Отмечаем в БД, что уведомление отправлено
                await delete_remind_by_task_id(task_id)
            except Exception as e:
                print(f"Ошибка при отправке напоминания: {e}")
        else:
            pass
