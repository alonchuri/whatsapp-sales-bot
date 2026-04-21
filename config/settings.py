import os
from dotenv import load_dotenv
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
FLIPPINGBOOK_API_KEY = os.getenv("FLIPPINGBOOK_API_KEY", "")
FLIPPINGBOOK_API_URL = os.getenv("FLIPPINGBOOK_API_URL", "https://api.flippingbook.com/v1")
TOKEN_FILE = "/tmp/google_token.json"
