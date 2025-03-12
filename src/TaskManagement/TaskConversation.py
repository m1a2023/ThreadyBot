from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from Enums import Priority

# Состояния диалога
TITLE, DESCRIPTION, PRIORITY = range(3)

class TaskConversation:

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("start")
        await update.message.reply_text("Введите название задачи:")
        return TITLE

    @staticmethod
    async def title(update: Update, context: ContextTypes.DEFAULT_TYPE):
        print("title")
        context.user_data["title"] = update.message.from_user
        await update.message.reply_text("Введите описание задачи:")
        return DESCRIPTION

    @staticmethod
    async def description(update: Update, context: ContextTypes.DEFAULT_TYPE):
        context.user_data["description"] = update.message.from_user

        keyboard = [["Высокий", "Средний", "Низкий"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

        await update.message.reply_text("Выберите приоритет задачи:", reply_markup=reply_markup)
        return PRIORITY

    @staticmethod
    async def priority(update: Update, context: ContextTypes.DEFAULT_TYPE):
        priority_map = {"Высокий": Priority.HIGH, "Средний": Priority.MEDIUM, "Низкий": Priority.LOW}
        context.user_data["priority"] = priority_map.get(update.message.text, Priority.MEDIUM)

        # Получаем данные задачи
        title = context.user_data["title"]
        description = context.user_data["description"]
        priority = context.user_data["priority"]

        # Создаём задачу
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Задача создана:\n*{title}*\n{description}\nПриоритет: {priority.name}",
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardRemove()
        )

        return ConversationHandler.END

    @staticmethod
    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отмена диалога"""
        await update.message.reply_text("Создание задачи отменено.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    @classmethod
    def get_conversation_handler(cls):
        """Возвращает обработчик для TaskManager"""
        return ConversationHandler(
            entry_points=[CommandHandler("add_task", cls.start)],
            states={
                TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.title)],
                DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.description)],
                PRIORITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, cls.priority)],
            },
            fallbacks=[CommandHandler("cancel", cls.cancel)],
        )
