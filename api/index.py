from fastapi import FastAPI, Request
import openai
from .sheets import log_to_sheet  # Note the dot for local import

app = FastAPI()

openai.api_key = "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"  

@app.post("/")
async def handle_call(request: Request):
    data = await request.json()

    user_input = data.get("SpeechResult", "Hello")

    # Use OpenAI to generate a response
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Sofia, a helpful legal assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        reply = response['choices'][0]['message']['content']

        # Log to Google Sheets (dummy for now)
        log_to_sheet({"input": user_input, "reply": reply})

        return {"reply": reply}

    except Exception as e:
        return {"error": str(e)}
