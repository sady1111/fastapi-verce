from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from twilio.twiml.voice_response import VoiceResponse

app = FastAPI()

@app.post("/call", response_class=PlainTextResponse)
async def call():
    response = VoiceResponse()
    response.say("Hello, this is Sofia from Legal Assist. I am calling regarding a recent accident you may have had.")
    response.pause(length=1)
    response.say("Can I please confirm, were you involved in a road traffic accident within the last 6 months?")
    return str(response)
