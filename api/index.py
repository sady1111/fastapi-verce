from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import openai
from twilio.twiml.voice_response import VoiceResponse
import os

app = FastAPI()

# Replace with your actual OpenAI API key
openai.api_key = "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"

@app.post("/voice")
async def voice(request: Request):
    form = await request.form()
    user_speech = form.get("SpeechResult", "")

    if not user_speech:
        response = VoiceResponse()
        response.say("Hello, this is Sofia from Legal Assist. Can I ask if you’ve had any kind of accident or injury in the last six months before August 2025?")
        response.gather(input="speech", timeout=5)
        return PlainTextResponse(str(response), media_type="application/xml")

    # Talk to OpenAI
    prompt = f"User said: {user_speech}\nYou are Sofia, a helpful virtual assistant for UK personal injury claims. Respond in a polite and helpful way, gather full accident information, and determine if user is eligible."
    
    try:
        reply = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Sofia, a kind and smart legal assistant who helps gather accident information."},
                {"role": "user", "content": user_speech}
            ],
            temperature=0.6
        )
        response_text = reply['choices'][0]['message']['content']
    except Exception as e:
        response_text = "An application error has occurred. Please try again later."

    response = VoiceResponse()
    response.say(response_text)
    response.gather(input="speech", timeout=5)
    return PlainTextResponse(str(response), media_type="application/xml")

@app.get("/")
def home():
    return {"message": "UK Personal Injury Bot Active - Legal Assist"}
