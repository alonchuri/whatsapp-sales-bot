import json
import os
import requests

QUESTIONS = [
    ("q1_purpose", "📋 *מה מטרת המצגת?*\nלדוגמה: הצעת מחיר, קטלוג מוצרים, סיכום פגישה"),
    ("q2_client",  "👤 *מה שם הלקוח / חברה?*"),
    ("q3_sender",  "✍️ *מה שמך (שם הסוכן)?*"),
    ("q4_notes",   "💬 *הערות נוספות? (אפשר לכתוב אין)*"),
]

STATE_FILE = "/tmp/bot_sessions.json"

def _load():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def _save(sessions):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False)

class ConversationHandler:
    def handle(self, sender, text, media_url, media_type):
        sessions = _load()
        session = sessions.get(sender, {"state": "IDLE", "answers": {}, "pdf_drive_id": None})
        if text and text.lower() in ("התחל", "start", "reset", "חדש"):
            session = {"state": "IDLE", "answers": {}, "pdf_drive_id": None}
            sessions[sender] = session
            _save(sessions)
            return self._welcome()
        reply = self._route(session, text, media_url, media_type)
        sessions[sender] = session
        _save(sessions)
        return reply

    def _route(self, session, text, media_url, media_type):
        state = session["state"]
        if state == "IDLE":
            if not media_url:
                return self._welcome()
            if "pdf" not in (media_type or "").lower():
                return "❌ אנא שלח קובץ PDF בלבד."
            try:
                from config.settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
                pdf_bytes = requests.get(media_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN), timeout=30).content
                session["pdf_bytes_len"] = len(pdf_bytes)
                session["pdf_bytes"] = pdf_bytes.hex()
                session["state"] = "Q0"
                return "✅ *קיבלתי את ה-PDF!*\n\n" + QUESTIONS[0][1]
            except Exception as e:
                return f"❌ שגיאה: {str(e)}"
        if state.startswith("Q"):
            idx = int(state[1:])
            if not text:
                return QUESTIONS[idx][1]
            session["answers"][QUESTIONS[idx][0]] = text
            next_idx = idx + 1
            if next_idx < len(QUESTIONS):
                session["state"] = f"Q{next_idx}"
                return QUESTIONS[next_idx][1]
            return self._process(session)
        return self._welcome()

    def _process(self, session):
        try:
            answers = session["answers"]
            agent = answers.get("q3_sender", "סוכן")
            client = answers.get("q2_client", "לקוח")
            session["state"] = "IDLE"
            session["answers"] = {}
            session["pdf_bytes"] = None
            return (f"🎉 *הלינק מוכן בקרוב!*\n\n👤 לקוח: {client}\n✍️ סוכן: {agent}\n"
                    f"📋 מטרה: {answers.get('q1_purpose','')}\n"
                    f"💬 הערות: {answers.get('q4_notes','')}\n\n"
                    f"🔗 חיבור Google Drive ו-FlippingBook יושלם בשלב הבא.\n\nלמצגת חדשה — שלח PDF נוסף 📎")
        except Exception as e:
            session["state"] = "IDLE"
            return f"❌ שגיאה: {str(e)}"

    def _welcome(self):
        return "👋 *ברוך הבא לבוט המכירות!*\n\n📎 שלח קובץ PDF ואני אכין לינק FlippingBook מוכן לשיתוף.\n\nלביטול — כתוב *חדש*"
