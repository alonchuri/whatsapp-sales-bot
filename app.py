import json
import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from handlers.conversation import ConversationHandler
from google_auth_oauthlib.flow import Flow
from services.drive import save_credentials
from config.settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

app = Flask(__name__)
handler = ConversationHandler()

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    num_media = int(request.values.get("NumMedia", 0))
    media_url = request.values.get("MediaUrl0", "") if num_media > 0 else None
    media_type = request.values.get("MediaContentType0", "") if num_media > 0 else None
    resp = MessagingResponse()
    msg = resp.message()
    reply = handler.handle(sender=sender, text=incoming_msg, media_url=media_url, media_type=media_type)
    msg.body(reply)
    return str(resp)

@app.route("/auth/google")
def auth_google():
    flow = Flow.from_client_config(
        {"web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uris": [GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }},
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt="consent", access_type="offline")
    return redirect(auth_url)

@app.route("/oauth/callback")
def oauth_callback():
    flow = Flow.from_client_config(
        {"web": {
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uris": [GOOGLE_REDIRECT_URI],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }},
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    flow.fetch_token(code=request.args.get("code"))
    save_credentials(flow.credentials)
    return "✅ גוגל דרייב מחובר בהצלחה! אפשר לסגור את הדף."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
