from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
import os
from twilio.rest import Client

app = FastAPI()

@app.post("/call")
async def call():
    # Your outbound call logic
    return {"message": "Call initiated"}

@app.post("/voice")
async def voice(request: Request):
    # Your voice response logic
    resp = VoiceResponse()
    resp.say("Hello, this is Sofia from Legal Assist. Can you tell me if you had an accident?")
    return PlainTextResponse(str(resp), media_type="application/xml")
