from fastapi import FastAPI, Request
from fastapi.responses import Response
import openai

app = FastAPI()

openai.api_key = "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"

@app.get("/")
async def root():
    return {"message": "UK Personal Injury Bot Active - Legal Assist"}

@app.post("/call")
async def voice_bot(request: Request):
    form_data = await request.form()
    user_input = form_data.get("SpeechResult", "")
    
    # Initial greeting or continue conversation
    if not user_input:
        prompt = (
            "You are Sofia, a friendly voice assistant working for Legal Assist. "
            "Call the person and say: 'Hello, this is Sofia from Legal Assist, calling about your personal injury claim. "
            "Have you had a road traffic accident or work-related injury in the past 6 months before August 2025?'"
        )
    else:
        prompt = (
            f"You are Sofia from Legal Assist. The caller said: '{user_input}'. "
            "Reply naturally as if you are a real human assistant handling their injury claim. "
            "Gather details like accident date, injury type, third-party involvement, and if a medical checkup happened. "
            "Ask relevant follow-up questions and handle objections. If they’re eligible, say a solicitor will call them soon."
        )

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    gpt_reply = response.choices[0].message["content"]

    twiml = f"""
    <Response>
        <Gather input="speech" timeout="3" speechTimeout="auto" action="/call" method="POST">
            <Say>{gpt_reply}</Say>
        </Gather>
        <Say>Sorry, I didn't catch that. Goodbye!</Say>
    </Response>
    """

    return Response(content=twiml.strip(), media_type="application/xml")
