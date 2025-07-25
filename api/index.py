from fastapi import FastAPI, Request
from fastapi.responses import Response
import openai
import os

app = FastAPI()

# Load API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}

@app.post("/api/call")
def call_handler():
    # Twilio will POST here first when the call starts
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
        form = await request.form()
        user_input = form.get("SpeechResult", "").strip()

        # Fallback if speech not captured
        if not user_input:
            twiml = """
            <Response>
                <Say voice="Polly.Joanna" language="en-GB">
                    Sorry, I didn't hear your response. A solicitor will call you shortly. Goodbye.
                </Say>
            </Response>
            """
            return Response(content=twiml.strip(), media_type="application/xml")

        # Ask ChatGPT how to respond
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Sofia, a professional legal assistant for personal injury claims."},
                {"role": "user", "content": f"The client said: '{user_input}'. How should Sofia respond professionally in one or two sentences before ending the call?"}
            ]
        )
        reply = gpt_response['choices'][0]['message']['content'].strip()

        # Final response
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
