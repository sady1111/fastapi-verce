from fastapi import FastAPI, Request
from fastapi.responses import Response
import openai

app = FastAPI()

# WARNING: This is your actual API key. Do not expose this in public or shared repos.
openai.api_key = "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"

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}

@app.post("/api/call")
async def call_handler(request: Request):
    body = await request.form()

    # Generate Sofia's intro with OpenAI
    gpt_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are Sofia, a professional claims assistant from Legal Assist. "
                    "You speak clearly and professionally, and ask about personal injury claims. "
                    "Ask if the caller had an accident in the last 6 months. Then end the call by saying a solicitor will call shortly."
                )
            },
            {
                "role": "user",
                "content": "Please greet the caller and ask them if they had an accident in the last six months."
            }
        ]
    )

    sofia_line = gpt_response['choices'][0]['message']['content']

    twiml = f"""
    <Response>
        <Say voice="Polly.Joanna" language="en-GB">
            {sofia_line}
        </Say>
        <Pause length="2"/>
        <Say voice="Polly.Joanna" language="en-GB">
            A solicitor will call you shortly. Thank you and have a great day.
        </Say>
        <Hangup/>
    </Response>
    """

    return Response(content=twiml.strip(), media_type="application/xml")
