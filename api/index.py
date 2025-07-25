import os
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import openai

# Set OpenAI API key
openai.api_key = "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"

app = FastAPI()

# Root route to avoid 404 error
@app.get("/")
async def root():
    return {"message": "Voice bot is running on Vercel."}

# Twilio-compatible voice endpoint
@app.post("/call")
async def handle_call(request: Request):
    try:
        body = await request.body()
        body_str = body.decode("utf-8")

        # Call OpenAI to get a response from the bot
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Sofia, a helpful AI voice assistant for personal injury claims."},
                {"role": "user", "content": body_str}
            ]
        )

        reply = response['choices'][0]['message']['content'].strip()

        # Return TwiML voice response
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say>{reply}</Say>
</Response>"""

        return PlainTextResponse(content=twiml, media_type="application/xml")

    except Exception as e:
        print("Error:", str(e))
        return PlainTextResponse(content="<Response><Say>Sorry, an error occurred.</Say></Response>", media_type="application/xml")
