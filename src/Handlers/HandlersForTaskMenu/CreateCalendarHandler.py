from datetime import datetime, timedelta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class CreateCalendar():
    @staticmethod
    def handle(year: int, month: int):
        keyboard = []
        
        # Заголовок календаря (месяц и год)
        month_name = datetime(year, month, 1).strftime("%B %Y")
        keyboard.append([InlineKeyboardButton(month_name, callback_data="ignore")])

        # Дни недели
        days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        keyboard.append([InlineKeyboardButton(day, callback_data="ignore") for day in days_of_week])

        # Первый день месяца
        first_day = datetime(year, month, 1)
        # Количество дней в месяце
        num_days = ((datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)) - timedelta(days=1)).day
        # Смещение для первого дня (0 - понедельник, 6 - воскресенье)
        offset = first_day.weekday()

        # Заполняем календарь
        row = []
        # Добавляем пустые ячейки для смещения
        row.extend([InlineKeyboardButton(" ", callback_data="ignore")] * offset)

        for day in range(1, num_days + 1):
            row.append(InlineKeyboardButton(str(day), callback_data=f"day_{year}_{month}_{day}"))
            if (day + offset) % 7 == 0:  # Если строка заполнена (7 дней)
                keyboard.append(row)
                row = []

        # Если последняя строка не пустая, добавляем пустые ячейки для выравнивания
        if row:
            row.extend([InlineKeyboardButton(" ", callback_data="ignore")] * (7 - len(row)))
            keyboard.append(row)

        # Кнопки для переключения месяцев
        prev_month = datetime(year, month, 1) - timedelta(days=1)
        next_month = datetime(year, month, 28) + timedelta(days=4)  # Переход к следующему месяцу
        keyboard.append([
            InlineKeyboardButton("← Предыдущий месяц", callback_data=f"prev_{prev_month.year}_{prev_month.month}"),
            InlineKeyboardButton("Следующий месяц →", callback_data=f"next_{next_month.year}_{next_month.month}")
        ])

        return InlineKeyboardMarkup(keyboard)