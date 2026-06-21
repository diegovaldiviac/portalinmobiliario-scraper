import os

from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER = os.getenv("TWILIO_WHATSAPP_FROM")
TO_NUMBER = os.getenv("TWILIO_WHATSAPP_TO")


def send_whatsapp_message(message):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        from_=FROM_NUMBER,
        to=TO_NUMBER,
        body=message,
    )
