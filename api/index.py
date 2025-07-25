from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
import os
import openai

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}

@app.post("/api/call")
def call_handler():
    # Sofia's opening line and gather
    twiml = """
    <Response>
        <Gather input="speech" action="/api/response" method="POST" timeout="5">
            <Say voice="Polly.Joanna" language="en-GB">
                Hello! This is Sofia from Legal Assist. Have you had an accident within the last six months?
            </Say>
        </Gather>
        <Say>I didn’t catch that. Goodbye.</Say>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")
