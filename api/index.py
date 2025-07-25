from fastapi import FastAPI, Request
from fastapi.responses import Response
import os
import openai

app = FastAPI()

# Load your OpenAI API key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}

@app.post("/api/call")
async def call_handler(request: Request):
    # Step 1: Get a GPT-generated message (simulate Sofia speaking)
    try:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Sofia, a helpful assistant for personal injury claims."},
                {"role": "user", "content": "Start the call professionally and ask if the user had an accident within the last six months."}
            ]
        )
        message = gpt_response["choices"][0]["message"]["content"]
    except Exception as e:
        message = "Hello! This is Sofia from Legal Assist. Did you have an accident within the last six months?"

    # Step 2: Create TwiML response
    twiml = f"""
    <Response>
        <Say voice="Polly.Joanna" language="en-GB">{message} A solicitor will call you shortly. Goodbye!</Say>
    </Response>
    """

    return Response(content=twiml.strip(), media_type="application/xml")
