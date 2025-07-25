from fastapi import FastAPI, Request
from fastapi.responses import Response
import openai
import os

app = FastAPI()

# Set your OpenAI API key directly here (not recommended for production)
openai.api_key = "sk-proj-REPLACE-WITH-YOUR-KEY"

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}

@app.post("/api/call")
def call_handler():
    # Twilio calls this endpoint when call starts
    twiml = """
    <Response>
        <Gather input="speech" speechTimeout="auto" timeout="8" action="/api/response" method="POST">
            <Say voice="Polly.Joanna" language="en-GB">
                Hello! This is Sofia from Legal Assist. Have you had an accident in the last six months?
         <Say voice="Polly.Joanna" language="en-GB">
            I didn’t catch that. A solicitor will call you shortly. Goodbye.
        </Say>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")

@app.post("/api/response")
async def process_response(request: Request):
    try:
        form = await request.form()
        print("🔍 Received form:", dict(form))  # DEBUG LOG
        user_input = form.get("SpeechResult", "").strip()
        print("🎤 User said:", user_input)

        if not user_input:
            twiml = """
            <Response>
                <Say voice="Polly.Joanna" language="en-GB">
                    Sorry, I didn’t hear your response. A solicitor will call you shortly. Goodbye.
                </Say>
            </Response>
            """
            return Response(content=twiml.strip(), media_type="application/xml")

        # Generate AI reply using OpenAI
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Sofia, a friendly legal assistant from Legal Assist. You help people with accident and injury claims."},
                {"role": "user", "content": f"The client said: '{user_input}'. How should Sofia respond in one or two friendly and professional sentences?"}
            ]
        )
        reply = gpt_response['choices'][0]['message']['content'].strip()

        print("💬 GPT reply:", reply)  # DEBUG LOG

        # Respond to Twilio
        twiml = f"""
        <Response>
            <Say voice="Polly.Joanna" language="en-GB">
                {reply} A solicitor will contact you shortly. Goodbye!
            </Say>
        </Response>
        """
        return Response(content=twiml.strip(), media_type="application/xml")

    except Exception as e:
        print("❌ Error occurred:", str(e))  # DEBUG LOG
        twiml = """
        <Response>
            <Say voice="Polly.Joanna" language="en-GB">
                An error occurred. A solicitor will contact you shortly. Goodbye.
            </Say>
        </Response>
        """
        return Response(content=twiml.strip(), media_type="application/xml")
