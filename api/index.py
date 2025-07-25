from fastapi import FastAPI, Request
from fastapi.responses import Response
import openai
import os

app = FastAPI()

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Replace with your actual Vercel domain (no trailing slash)
VERCEL_DOMAIN = "https://fastapi-vercel-murex.vercel.app"

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}


@app.post("/api/call")
def call_handler():
    # Initial Twilio response to start the conversation
    twiml = f"""
    <Response>
        <Gather input="speech" action="{VERCEL_DOMAIN}/api/response" method="POST" timeout="5">
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
        form = await request.form()
        user_input = form.get("SpeechResult", "").strip()
        print("User said:", user_input)

        # Fallback if no speech detected
        if not user_input:
            twiml = """
            <Response>
                <Say voice="Polly.Joanna" language="en-GB">
                    Sorry, I didn't hear your response. A solicitor will call you shortly. Goodbye.
                </Say>
            </Response>
            """
            return Response(content=twiml.strip(), media_type="application/xml")

        # Ask OpenAI GPT how Sofia should respond
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",  # or use "gpt-3.5-turbo" if needed
            messages=[
                {
                    "role": "system",
                    "content": "You are Sofia, a friendly and professional legal assistant helping clients with personal injury claims in the UK. Answer clearly and briefly."
                },
                {
                    "role": "user",
                    "content": f"The client said: '{user_input}'. How should Sofia respond professionally in one or two sentences before ending the call?"
                }
            ]
        )
        reply = gpt_response['choices'][0]['message']['content'].strip()
        print("GPT reply:", reply)

        # Final TwiML response
        twiml = f"""
        <Response>
            <Say voice="Polly.Joanna" language="en-GB">
                {reply} A solicitor will contact you shortly. Goodbye!
            </Say>
        </Response>
        """
        return Response(content=twiml.strip(), media_type="application/xml")

    except Exception as e:
        print("Error:", e)
        twiml = """
        <Response>
            <Say voice="Polly.Joanna" language="en-GB">
                An error occurred. A solicitor will contact you shortly. Goodbye.
            </Say>
        </Response>
        """
        return Response(content=twiml.strip(), media_type="application/xml")
