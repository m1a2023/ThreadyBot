import logging
from telegram.ext import Application

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

class BotApp:
    _instance = None

    def __new__(cls, token=None):
        if cls._instance is None:
            if token is None:
                raise ValueError("Token must be provided for the first instantiation")
            cls._instance = super().__new__(cls)
            cls._instance.application = Application.builder().token(token).build()
        return cls._instance

    def get_application(self):
        return self._instance.application
