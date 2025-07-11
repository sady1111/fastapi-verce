from fastapi import FastAPI, Request
from twilio.rest import Client
import os

app = FastAPI()

# Load environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.environ.get("TWILIO_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.get("/")
def root():
    return {"message": "Hello from FastAPI!"}

@app.post("/call")
async def make_call(request: Request):
    data = await request.json()
    to_number = data.get("to")

    if not to_number:
        return {"error": "Missing 'to' number"}

    try:
        call = client.calls.create(
            to=to_number,
            from_=TWILIO_NUMBER,
            twiml='<Response><Say>Hello! This is a test call from your FastAPI app.</Say></Response>'
        )
        return {"status": "Call initiated", "call_sid": call.sid}
    except Exception as e:
        return {"error": str(e)}
