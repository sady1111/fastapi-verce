from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
import openai
import os
import logging

app = FastAPI()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.get("/")
def root():
    return {"message": "Voice bot is running on Vercel."}

@app.post("/api/call")
def call_handler():
    # Initial greeting when call starts
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
        form = await request.body()
        data = form.decode()
        
        # Parse the SpeechResult manually from raw body
        import urllib.parse
        parsed = urllib.parse.parse_qs(data)
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

        # Get response from OpenAI
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are Sofia, a helpful legal assistant for personal injury claims in the UK."},
                {"role": "user", "content": f"The client said: '{user_input}'. How should Sofia respond professionally in one or two polite sentences before ending the call?"}
            ]
        )

        reply = gpt_response["choices"][0]["message"]["content"].strip()

        # TwiML response with GPT reply
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
