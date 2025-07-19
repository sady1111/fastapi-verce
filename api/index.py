from fastapi import FastAPI, Request, Form
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse
import os

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins (for testing only — restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/call", response_class=PlainTextResponse)
async def call():
    response = VoiceResponse()
    response.say("Hello, this is Sofia from Legal Assist. I am calling regarding a recent accident you may have had.")
    response.pause(length=1)
    response.say("Can I please confirm, were you involved in a road traffic accident within the last 6 months?")
    return str(response)
