import os
from dotenv import load_dotenv
load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
GOOGLE_SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "service_account.json")
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
FLIPPINGBOOK_API_KEY = os.getenv("FLIPPINGBOOK_API_KEY", "")
FLIPPINGBOOK_API_URL = os.getenv("FLIPPINGBOOK_API_URL", "https://api.flippingbook.com/v1")
