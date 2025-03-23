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

class UserReportHandler(Handler):
    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        report = await get_report_by_project_id(7) #покатак

        file_path = f"project_report_{7}.pdf"
        await UserReportHandler.generate_pdf(report, file_path)

        # Отправляем пользователю
        with open(file_path, "rb") as pdf_file:
            print("done")
            await update.callback_query.message.reply_document(document=pdf_file, filename=f"Report_{7}.pdf")

        # Можно удалить файл после отправки (если не нужен локально)
        import os
        os.remove(file_path)
