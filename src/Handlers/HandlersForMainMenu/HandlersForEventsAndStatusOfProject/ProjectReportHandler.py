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
from reportlab.pdfgen import canvas

from Handlers.Handler import Handler
from Handlers.RequestsHandler import get_report_by_project_id

class ProjectReportHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        report = await get_report_by_project_id(7) #покатак

        file_path = f"project_report_{7}.pdf"
        await ProjectReportHandler.generate_pdf(report, file_path)

        # Отправляем пользователю
        with open(file_path, "rb") as pdf_file:
            print("done")
            await update.callback_query.message.reply_document(document=pdf_file, filename=f"Report_{7}.pdf")

        # Можно удалить файл после отправки (если не нужен локально)
        import os
        os.remove(file_path)

    @staticmethod
    async def generate_pdf(report_data: dict, file_path: str):
        doc = SimpleDocTemplate(file_path, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

        # Стили для текста
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

        # Заголовок отчета
        title = Paragraph(f"Отчет по проекту: {report_data['project_title']}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))

        # Статистика задач
        task_stats = [
            [Paragraph("Категория", header_style), Paragraph("Количество", header_style), Paragraph("Доля", header_style)],
            [Paragraph("Всего задач", body_style), report_data['total_quantity_of_tasks'], "100%"],
            [Paragraph("Завершено", body_style), report_data['quantity_of_compleated_tasks'],
            f"{int(report_data['quantity_of_compleated_tasks']/report_data['total_quantity_of_tasks']*100)}%"],
            [Paragraph("В процессе", body_style), report_data['quantity_of_tasks_in_progress'],
            f"{int(report_data['quantity_of_tasks_in_progress']/report_data['total_quantity_of_tasks']*100)}%"],
            [Paragraph("Ожидают выполнения", body_style), report_data['quantity_of_todo_tasks'],
            f"{int(report_data['quantity_of_todo_tasks']/report_data['total_quantity_of_tasks']*100)}%"],
            [Paragraph("Просрочено", body_style), report_data['quantity_of_overdue_tasks'],
            f"{int(report_data['quantity_of_overdue_tasks']/report_data['total_quantity_of_tasks']*100)}%"]
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

        # Топ разработчики
        devs = [
            [Paragraph("🏆 Самый ценный:", body_style), Paragraph(str(report_data['most_valuable_developer']), body_style)],
            [Paragraph("⚡ Самый продуктивный:", body_style), Paragraph(str(report_data['most_productive_developer']), body_style)],
            [Paragraph("⚠️ Требует внимания:", body_style), Paragraph(str(report_data['most_flawed_developer']), body_style)]
        ]

        dev_table = Table(devs, colWidths=[5*cm, 11*cm])
        dev_table.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), 'DejaVuSans'),
            ('FONTSIZE', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,0), 'LEFT'),
            ('BACKGROUND', (0,0), (0,-1), colors.lightgrey)
        ]))

        elements.append(Paragraph("Топ разработчики", header_style))
        elements.append(Spacer(1, 0.3*cm))
        elements.append(dev_table)
        elements.append(Spacer(1, 1*cm))

        # Генерация PDF
        doc.build(elements)
