import os
from dotenv import load_dotenv

load_dotenv()

IAM_TOKEN = os.getenv("IAM_TOKEN")
FOLDER_ID = os.getenv("FOLDER_ID")
TG_TOKEN = os.getenv("TG_TOKEN")
