from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from twilio.rest import Client
import os

app = FastAPI()

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

# Create Twilio client only if credentials exist
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
else:
    client = None

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello from FastAPI on Vercel!"})

@app.post("/call")
async def make_call(request: Request):
    if not client:
        return JSONResponse(content={"error": "Twilio client not initialized."}, status_code=500)

    try:
        data = await request.json()
        to_number = data.get("to")

        if not to_number:
            return JSONResponse(content={"error": "Missing 'to' phone number."}, status_code=400)

        call = client.calls.create(
            to=to_number,
            from_=TWILIO_NUMBER,
            twiml="<Response><Say>Hello! This is a test call from your FastAPI app.</Say></Response>"
        )

        return JSONResponse(content={"status": "Call initiated", "call_sid": call.sid})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
