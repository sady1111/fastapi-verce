from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from twilio.rest import Client

app = FastAPI()

# ✅ Twilio credentials (already available to you)
TWILIO_ACCOUNT_SID = "AC4b424c8cbe37274f2e51d38251f64346"
TWILIO_AUTH_TOKEN = "9f3e3cd9d1b5ef96f34d4f016b9ff1a2"
TWILIO_PHONE_NUMBER = "+447412403311"  # Your verified Twilio number

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
    # TwiML XML response that Twilio will speak
    twiml = """
    <Response>
        <Say voice="Polly.Amy" language="en-GB">
            Hello, this is Sofia from Legal Assist. I'm here to ask a few quick questions about a recent accident or injury.
        </Say>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")

