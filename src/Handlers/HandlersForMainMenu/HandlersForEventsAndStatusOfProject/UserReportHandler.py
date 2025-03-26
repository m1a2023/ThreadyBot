from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart

from Handlers.Handler import Handler
from Handlers.RequestsHandler import get_report_by_user_id

import os

class UserReportHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = context.user_data["chosenDeveloper"] # id выбранного разработчика для формирования отчета
        project_id = context.user_data["chosenProject"] # id выбранного проекта для формирования отчета

        report = await get_report_by_user_id(user_id) #покатак

        file_path = f"Developer_report_{user_id}.pdf"
        await UserReportHandler.generate_pdf(report, file_path)

        # Отправляем пользователю
        with open(file_path, "rb") as pdf_file:
            print("done")
            await update.callback_query.message.reply_document(document=pdf_file, filename=f"Developer_report_{user_id}.pdf")

        # Можно удалить файл после отправки (если не нужен локально)
        os.remove(file_path)

    @staticmethod
    async def generate_pdf(report_data: dict, file_path: str):
        tasks = report_data['all_users_tasks_duration']

        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements = []

        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

        title_style = ParagraphStyle(
            name="Title",
            fontSize=18,
            leading=24,
            alignment=TA_CENTER,
            fontName="DejaVuSans-Bold"
        )

        header_style = ParagraphStyle(
            name="Header",
            fontSize=14,
            leading=18,
            fontName="DejaVuSans-Bold",
            textColor=colors.darkblue
        )

        body_style = ParagraphStyle(
            name="Body",
            fontSize=12,
            leading=14,
            fontName="DejaVuSans"
        )

        title = Paragraph(f"Отчет по разработчику: {report_data['developer_name']}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))

        task_stats = [
            [Paragraph("Категория", header_style), Paragraph("Количество", header_style), Paragraph("Доля", header_style)],
            [Paragraph("Всего задач", body_style), report_data['all_tasks'], "100%"],

            [
            Paragraph("Завершено", body_style), report_data['total_completed_tasks'],
            f"{int(report_data['total_completed_tasks']/report_data['all_tasks']*100)}%"
            ],

            [
            Paragraph("В процессе", body_style), report_data['total_in_progress_tasks'],
            f"{int(report_data['total_in_progress_tasks']/report_data['all_tasks']*100)}%"
            ],

            [
            Paragraph("Ожидают выполнения", body_style), report_data['total_todo_tasks'],
            f"{int(report_data['total_todo_tasks']/report_data['all_tasks']*100)}%"
            ],

            [
            Paragraph("Просрочено", body_style), report_data['total_overdue_tasks'],
            f"{int(report_data['total_overdue_tasks']/report_data['all_tasks']*100)}%"
            ]
        ]

        task_table = Table(task_stats, colWidths=[8*cm, 4*cm, 4*cm])
        task_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))

        elements.append(Paragraph("Статистика задач", header_style))
        elements.append(Spacer(1, 0.3*cm))
        elements.append(task_table)
        elements.append(Spacer(1, 1*cm))

        elements.append(Paragraph("Гистограма всех задач и времени их выполнения", header_style))
        elements.append(Spacer(1, 1*cm))
        await UserReportHandler.generate_vertical_bar_chart(tasks, elements)
        elements.append(Spacer(1, 1*cm))

        tasks_dur = [
            [Paragraph("Категория", header_style), Paragraph("Название задачи", header_style), Paragraph("Колличество часов", header_style)],
            [
                Paragraph("Наименее времязатратная задача", body_style),
                Paragraph(f"{report_data['the_easiest_task']['title']}"),
                Paragraph(f"{report_data['the_easiest_task']['duration']}")
            ],
            [
                Paragraph("Самая времязатратная задача", body_style),
                Paragraph(f"{report_data['most_dificult_task']['title']}"),
                Paragraph(f"{report_data['most_dificult_task']['duration']}")
            ],
            [
                Paragraph("Общее время, потраченное на задачи", body_style),
                Paragraph("-"),
                Paragraph(f"{report_data['total_hours_worked']}")
            ]
        ]

        dev_table = Table(tasks_dur, colWidths=[7*cm, 4*cm])
        dev_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))

        elements.append(Paragraph("Дополнительная информация", header_style))
        elements.append(Spacer(1, 0.3*cm))
        elements.append(dev_table)
        elements.append(Spacer(1, 1*cm))

        doc.build(elements)

    @staticmethod
    async def generate_vertical_bar_chart(tasks: dict, elements):
        ready_times = []
        not_ready_times = []
        category_names = []

        for task_name, task_info in tasks.items():
            category_names.append(task_name)
            if task_info['is_done'] == "true":
                ready_times.append(task_info['duration'])
                not_ready_times.append(0)  # Для неготовых задач ставим 0
            else:
                not_ready_times.append(task_info['duration'])
                ready_times.append(0)  # Для готовых задач ставим 0

        drawing = Drawing(400, 170)

        # Создаем гистограмму
        chart = VerticalBarChart()
        chart.width = 350
        chart.height = 150
        chart.x = 30
        chart.y = 30

        # Данные для графика (две серии)
        chart.data = [ready_times, not_ready_times]

        # Настройка категорий
        chart.categoryAxis.categoryNames = category_names
        chart.categoryAxis.labels.angle = 45
        chart.categoryAxis.labels.dy = -15

        # Настройка цветов
        chart.bars[0].fillColor = colors.blue  # Готовые задачи
        chart.bars[1].fillColor = colors.red   # Неготовые задачи

        # Добавляем график на холст
        drawing.add(chart)

        elements.append(drawing)
