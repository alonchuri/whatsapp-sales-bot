import io
import json
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from config.settings import (
    GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI, GOOGLE_DRIVE_FOLDER_ID, TOKEN_FILE
)

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

def get_credentials():
    if not os.path.exists(TOKEN_FILE):
        return None
    with open(TOKEN_FILE, "r") as f:
        token_data = json.load(f)
    creds = Credentials(
        token=token_data.get("token"),
        refresh_token=token_data.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        scopes=SCOPES
    )
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        save_credentials(creds)
    return creds

def save_credentials(creds):
    with open(TOKEN_FILE, "w") as f:
        json.dump({
            "token": creds.token,
            "refresh_token": creds.refresh_token
        }, f)

class DriveService:
    def __init__(self):
        creds = get_credentials()
        if not creds:
            raise Exception("Google Drive לא מחובר")
        self.service = build("drive", "v3", credentials=creds, cache_discovery=False)

    def upload_pdf(self, pdf_bytes: bytes, filename: str):
        file_metadata = {"name": filename, "parents": [GOOGLE_DRIVE_FOLDER_ID]}
        media = MediaIoBaseUpload(io.BytesIO(pdf_bytes), mimetype="application/pdf", resumable=True)
        file = self.service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()
        return file["id"], file.get("webViewLink", "")
