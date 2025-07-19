from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import os
import openai

# Twilio credentials
TWILIO_ACCOUNT_SID = "AC312ed40bc95fecde9f15a8083cc2e257"
TWILIO_AUTH_TOKEN = "9a2de14abf9bbae4adec1566e8994476"
TWILIO_FROM_NUMBER = "+447412403311"

# OpenAI key
openai.api_key = "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"

app = FastAPI()

@app.post("/call")
async def make_call():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        twiml='<Response><Say voice="alice">Hello, this is Sofia from Legal Assist. Can you tell me if you had an accident recently?</Say></Response>',
        to="+447514115780",  # Replace with recipient number
        from_=TWILIO_FROM_NUMBER
    )
    return {"status": "initiated", "sid": call.sid}

@app.post("/voice")
async def voice_response(request: Request):
    form = await request.form()
    user_input = form.get("SpeechResult") or ""

    # Get response from OpenAI
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're Sofia from Legal Assist, helping users with personal injury claims."},
            {"role": "user", "content": user_input}
        ]
    )
    reply = completion.choices[0].message.content

    response = VoiceResponse()
    response.say(reply, voice="Polly.Joanna", language="en-GB")
    return PlainTextResponse(str(response), media_type="application/xml")
