from fastapi import FastAPI
from fastapi.responses import Response

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}

@app.post("/api/call")
def call_handler():
    twiml = """
    <Response>
        <Say voice="Polly.Joanna" language="en-GB">
            Hello! This is Sofia from Legal Assist. How can I help you with your personal injury claim today?
        </Say>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")
