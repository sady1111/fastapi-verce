from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import openai
import os

app = FastAPI()

# Set your OpenAI API key here
openai.api_key = "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"

@app.post("/call")
async def call_handler(request: Request):
    form = await request.form()
    from_number = form.get("From", "Unknown")
    user_input = form.get("SpeechResult", "No input received.")

    # AI Voice Assistant response
    prompt = f"You are Sofia, a polite and professional personal injury assistant. The caller said: '{user_input}'. Respond like a human, naturally."
    
    try:
        ai_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Sofia, an expert in personal injury claims in the UK."},
                {"role": "user", "content": prompt}
            ]
        )
        reply_text = ai_response.choices[0].message.content.strip()
    except Exception as e:
        rep
