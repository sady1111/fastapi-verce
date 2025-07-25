from fastapi import FastAPI, Request
from fastapi.responses import Response
import openai
import os
import logging
import urllib.parse

app = FastAPI()

# Configure OpenAI using new SDK (>=1.0)
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}


@app.post("/api/call")
def call_handler():
    # Initial greeting
    twiml = """
    <Response>
        <Gather input="speech" action="/api/response" method="POST" timeout="5">
            <Say voice="Polly.Joanna" language="en-GB">
                Hello! This is Sofia from Legal Assist. Have you had an accident in the last six months?
            </Say>
        </Gather>
        <Say>I didn’t catch that. Goodbye.</Say>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")


@app.post("/api/response")
async def process_response(request: Request):
    try:
        # Read raw form data and decode
        raw_body = await request.body()
        parsed = urllib.parse.parse_qs(raw_body.decode())
        user_input = parsed.get("SpeechResult", [""])[0].strip()

        if not user_input:
            twiml = """
            <Response>
                <Say voice="Polly.Joanna" language="en-GB">
                    Sorry, I didn't hear your response. A solicitor will call you shortly. Goodbye.
                </Say>
            </Response>
            """
            return Response(content=twiml.strip(), media_type="application/xml")

        # Call OpenAI using new SDK
        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Sofia, a helpful legal assistant for personal injury claims in the UK."},
                {"role": "user", "content": f"The client said: '{user_input}'. How should Sofia respond in a polite and professional way before ending the call?"}
            ]
        )

        reply = chat_completion.choices[0].message.content.strip()

        # Respond with GPT reply
        twiml = f"""
        <Response>
            <Say voice="Polly.Joanna" language="en-GB">
                {reply} A solicitor will contact you shortly. Goodbye!
            </Say>
        </Response>
        """
        return Response(content=twiml.strip(), media_type="application/xml")

    except Exception as e:
        logging.error(f"Error in /api/response: {e}")
        twiml = """
        <Response>
            <Say voice="Polly.Joanna" language="en-GB">
                An error occurred. A solicitor will contact you shortly. Goodbye.
            </Say>
        </Response>
        """
        return Response(content=twiml.strip(), media_type="application/xml")
