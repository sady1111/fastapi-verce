from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
import openai
import os

app = FastAPI()

# === YOUR SECRETS ===
TWILIO_ACCOUNT_SID = "AC312ed40bc95fecde9f15a8083cc2e257"
TWILIO_AUTH_TOKEN = "9a2de14abf9bbae4adec1566e8994476"
TWILIO_FROM_NUMBER = "+447412403311"
OPENAI_API_KEY = "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"

# === SETUP CLIENTS ===
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai.api_key = OPENAI_API_KEY

# === 1. CALL INITIATOR ===
@app.post("/call")
async def make_call(to: str = Form(...)):
    call = client.calls.create(
        to=to,
        from_=TWILIO_FROM_NUMBER,
        url="https://fastapi-vercel-murex.vercel.app/voice"
    )
    return {"status": "success", "call_sid": call.sid}

# === 2. VOICE HANDLER ===
@app.post("/voice")
async def voice(request: Request):
    form = await request.form()
    speech_result = form.get("SpeechResult", "").strip()

    if not speech_result:
        # FIRST LINE OF THE CALL (INITIAL PROMPT)
        response = VoiceResponse()
        response.say("Hi, this is Sofia from Legal Assist. I’m calling about a recent accident. Have you or someone you know been involved in a non-fault accident in the last 2 years?", voice='Polly.Joanna', language='en-GB')
        response.gather(input="speech", action="/voice", method="POST")
        return PlainTextResponse(str(response), media_type="application/xml")

    # GENERATE AI REPLY USING OPENAI
    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are Sofia, a helpful legal assistant for personal injury claims in the UK. Always respond conversationally."},
            {"role": "user", "content": speech_result}
        ]
    )

    reply = completion.choices[0].message.content.strip()

    response = VoiceResponse()
    response.say(reply, voice='Polly.Joanna', language='en-GB')
    response.gather(input="speech", action="/voice", method="POST")
    return PlainTextResponse(str(response), media_type="application/xml")

