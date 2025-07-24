from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from datetime import datetime
import openai
from sheets import log_to_sheet  # This should exist in sheets.py

app = FastAPI()

# Your actual OpenAI API key
openai.api_key = "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"

# Store conversations in memory
conversation_history = {}

@app.post("/voice")
async def voice_webhook(request: Request):
    form = await request.form()
    user_input = form.get("SpeechResult")
    call_sid = form.get("CallSid") or "unknown"

    if not user_input:
        xml = """
        <?xml version='1.0' encoding='UTF-8'?>
        <Response>
            <Say>Hi, this is Sofia from Legal Assist. I didn’t catch that. Can you repeat please?</Say>
            <Pause length='2'/>
            <Redirect>/voice</Redirect>
        </Response>
        """
        return PlainTextResponse(content=xml.strip(), media_type="application/xml")

    # Start new conversation if needed
    if call_sid not in conversation_history:
        conversation_history[call_sid] = [
            {
                "role": "system",
                "content": (
                    "You are Sofia, a professional assistant from Legal Assist. "
                    "Your task is to conduct personal injury claim intakes. Collect: full name, accident date, type of accident, injuries, fault, and any medical treatment. "
                    "Ask one question at a time, respond naturally like a human, and answer user questions too. "
                    "End by saying: 'Thank you. Our solicitor will call you shortly.'"
                )
            }
        ]

    # Add user message
    conversation_history[call_sid].append({"role": "user", "content": user_input})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history[call_sid]
        )
        ai_reply = completion.choices[0].message.content.strip()
        conversation_history[call_sid].append({"role": "assistant", "content": ai_reply})
    except Exception:
        ai_reply = "Sorry, something went wrong. Our solicitor will call you shortly."

    # Log to Google Sheet
    log_to_sheet(call_sid, user_input, ai_reply)

    # Check if it’s time to end the call
    if any(phrase in ai_reply.lower() for phrase in [
        "our solicitor will call you shortly",
        "we will contact you",
        "thank you for your time"
    ]):
        xml = f"""
        <?xml version='1.0' encoding='UTF-8'?>
        <Response>
            <Say>{ai_reply}</Say>
            <Hangup/>
        </Response>
        """
    else:
        xml = f"""
        <?xml version='1.0' encoding='UTF-8'?>
        <Response>
            <Say>{ai_reply}</Say>
            <Pause length='1'/>
            <Redirect>/voice</Redirect>
        </Response>
        """

    return PlainTextResponse(content=xml.strip(), media_type="application/xml")
