# config.py

import os
from dotenv import load_dotenv

load_dotenv()

API_SECRET = os.getenv("API_SECRET")
PORT = int(os.getenv("PORT", 8000))

DOWNLOAD_DIR = "downloads"
TEMP_DIR = "temp"
TOKEN_EXPIRY = 120

os.makedirs(DOWNLOAD_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
