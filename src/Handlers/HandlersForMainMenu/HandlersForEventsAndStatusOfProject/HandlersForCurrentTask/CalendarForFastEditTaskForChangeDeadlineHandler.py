from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes
from typing import Any

from Handlers.Handler import Handler
from Handlers.HandlersForTaskMenu.CreateCalendarHandler import CreateCalendar

class CalendarForFastEditTaskForChangeDeadlineHandler(Handler):
    @staticmethod
    async def handle(update, context, year = None, month = None):
        query = update.callback_query
        await query.answer()

        context.user_data["state"] = "fastEditTaskDeadline"
        
        # Если год и месяц не переданы, используем текущую дату
        if year is None or month is None:
            current_date = datetime.now()
            year = current_date.year 
            month = current_date.month
        
        calendar_id = context.user_data.get("calendar_id")

        if calendar_id:
            # Редактируем существующее сообщение
            await query.edit_message_text("Выберите дату:",reply_markup=CreateCalendar.handle(year, month))
        else:
            # Отправляем новое сообщение с календарем
            sent_message = await query.message.reply_text("Выберите дату:", reply_markup=CreateCalendar.handle(year, month))
            context.user_data["bot_message_id"] = sent_message.message_id
            context.user_data["calendar_id"] = sent_message.message_id
