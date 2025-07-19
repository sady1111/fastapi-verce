from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from twilio.rest import Client
import os

app = FastAPI()

# Load Twilio credentials from environment or hardcode them (for testing only)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid_here")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token_here")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+1234567890")  # Your Twilio number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class CallRequest(BaseModel):
    to: str

@app.post("/call")
async def initiate_call(call_request: CallRequest):
    try:
        call = client.calls.create(
            to=call_request.to,
            from_=TWILIO_PHONE_NUMBER,
            url="https://fastapi-vercel-git-main-saddams-projects-44ca5472.vercel.app/voice"
        )
        return {"status": "initiated", "sid": call.sid}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/voice")
async def voice_response(request: Request):
    # TwiML XML response
    twiml = """
    <Response>
        <Say voice="Polly.Amy" language="en-GB">
            Hello, this is Sofia from Legal Assist. I'm here to ask a few quick questions about a recent accident or injury.
        </Say>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")
