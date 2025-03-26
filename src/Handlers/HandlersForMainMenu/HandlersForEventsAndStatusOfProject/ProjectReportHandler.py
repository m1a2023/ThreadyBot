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
from reportlab.graphics.charts.legends import Legend

import os

from Handlers.Handler import Handler
from Handlers.RequestsHandler import get_report_by_project_id

class ProjectReportHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        proj_id = context.user_data["chosenProject"]

        report = await get_report_by_project_id(proj_id)

        file_path = f"Project_report_{proj_id}.pdf"
        await ProjectReportHandler.generate_pdf(report, file_path)

        # Отправляем пользователю
        with open(file_path, "rb") as pdf_file:
            print("done")
            await update.callback_query.message.reply_document(document=pdf_file, filename=f"Project_report_{proj_id}.pdf")

        os.remove(file_path)

    @staticmethod
    async def generate_pdf(report_data: dict, file_path: str):
        tasks = report_data['all_tasks_in_project_with_duration']

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

        title = Paragraph(f"Отчет по проекту: {report_data['project_title']}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))

        task_stats = [
            [Paragraph("Категория", header_style), Paragraph("Количество", header_style), Paragraph("Доля", header_style)],
            [Paragraph("Всего задач", body_style), report_data['total_quantity_of_tasks'], "100%"],

            [
            Paragraph("Завершено", body_style), report_data['quantity_of_completed_tasks'],
            f"{int(report_data['quantity_of_completed_tasks']/report_data['total_quantity_of_tasks']*100)}%"
            ],

            [
            Paragraph("В процессе", body_style), report_data['quantity_of_tasks_in_progress'],
            f"{int(report_data['quantity_of_tasks_in_progress']/report_data['total_quantity_of_tasks']*100)}%"
            ],

            [
            Paragraph("Ожидают выполнения", body_style), report_data['quantity_of_todo_tasks'],
            f"{int(report_data['quantity_of_todo_tasks']/report_data['total_quantity_of_tasks']*100)}%"
            ],

            [
            Paragraph("Просрочено", body_style), report_data['quantity_of_overdue_tasks'],
            f"{int(report_data['quantity_of_overdue_tasks']/report_data['total_quantity_of_tasks']*100)}%"
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
        await ProjectReportHandler.generate_vertical_bar_chart(tasks, elements, body_style)
        elements.append(Spacer(1, 2*cm))

        devs = [
            [Paragraph("Категория", header_style), Paragraph("Имя", header_style), Paragraph("Статистика", header_style)],
            [
                Paragraph("Самый ценный", body_style),
                Paragraph(f"{report_data['most_valuable_developer']['name']}"),
                Paragraph(f"Эффективность: {report_data['most_valuable_developer']['effectiveness']}%", body_style)
            ],
            [
                Paragraph("Самый продуктивный", body_style),
                Paragraph(f"{report_data['most_productive_developer']['name']}"),
                Paragraph(f"Завершено задач: {report_data['most_productive_developer']['quantity']}", body_style)
            ],
            [
                Paragraph("Требует внимания", body_style),
                Paragraph(f"{report_data['most_flawed_developer']['name']}"),
                Paragraph(f"Просрочено задач: {report_data['most_flawed_developer']['quantity']}", body_style)
            ]
        ]

        dev_table = Table(devs, colWidths=[6*cm, 3*cm, 6*cm])
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

        elements.append(Paragraph("Выделяющиеся разработчики", header_style))
        elements.append(Spacer(1, 0.3*cm))
        elements.append(dev_table)
        elements.append(Spacer(1, 1*cm))

        doc.build(elements)

    @staticmethod
    async def generate_vertical_bar_chart(tasks: dict, elements, style):
        ready_times = []
        not_ready_times = []
        allotted_times = []
        task_numbers = []  # Номера задач вместо названий
        task_names = {}    # Соответствие номеров и названий

        # Генерируем нумерацию задач
        for idx, (task_name, task_info) in enumerate(tasks.items(), 1):
            task_numbers.append(str(idx))
            task_names[str(idx)] = task_name  # Сохраняем соответствие номер-название

            # Заполняем данные
            actual_time = task_info['duration']
            allotted_time = task_info['allotted_time']

            if task_info['is_done'] == "true":
                ready_times.append(actual_time)
                not_ready_times.append(0)
            else:
                not_ready_times.append(actual_time)
                ready_times.append(0)

            allotted_times.append(allotted_time)

        drawing = Drawing(500, 400)

        # Гистограмма
        chart = VerticalBarChart()
        chart.width = 450
        chart.height = 200
        chart.x = 20
        chart.y = 170

        # Настройка данных
        chart.data = [ready_times, not_ready_times, allotted_times]

        # Нумерованные категории
        chart.categoryAxis.categoryNames = task_numbers
        chart.categoryAxis.labels.fontSize = 8
        chart.categoryAxis.labels.angle = 0  # Горизонтальные подписи

        # Цвета столбцов
        chart.bars[0].fillColor = colors.green
        chart.bars[1].fillColor = colors.red
        chart.bars[2].fillColor = colors.blue

        # Легенда с нумерацией задач
        legend = Legend()
        legend.x = 20
        legend.y = 100
        legend.colorNamePairs = [

            (colors.green, 'Фактическое (выполнено)'),
            (colors.red, 'Фактическое (не выполнено)'),
            (colors.blue, 'Плановое время')
        ]
        legend.fontName = 'DejaVuSans'
        legend.fontSize = 8
        legend.columnMaximum = 3  # Колонки для компактного отображения

        tasks_text = [
            "Нумерация задач:",
            *[f"{num}. {name}" for num, name in task_names.items()],
        ]

        drawing.add(chart)
        drawing.add(legend)
        elements.append(drawing)

        for line in tasks_text:
            p = Paragraph(line, style)
            elements.append(p)
            elements.append(Spacer(1, 5))
