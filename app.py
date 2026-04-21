from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from handlers.conversation import ConversationHandler

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
    reply = handler.handle(
        sender=sender,
        text=incoming_msg,
        media_url=media_url,
        media_type=media_type,
    )
    msg.body(reply)
    return str(resp)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
