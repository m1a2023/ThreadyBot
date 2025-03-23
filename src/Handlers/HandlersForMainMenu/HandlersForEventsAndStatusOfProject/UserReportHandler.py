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
from Handlers.RequestsHandler import get_report_by_user_id

import os

class UserReportHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        report = await get_report_by_user_id(7) #покатак

        file_path = f"Developer_report_{7}.pdf"
        await UserReportHandler.generate_pdf(report, file_path)

        # Отправляем пользователю
        with open(file_path, "rb") as pdf_file:
            print("done")
            await update.callback_query.message.reply_document(document=pdf_file, filename=f"Developer_report_{7}.pdf")

        # Можно удалить файл после отправки (если не нужен локально)
        os.remove(file_path)

    @staticmethod
    async def generate_pdf(report_data: dict, file_path: str):
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
