from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from datetime import datetime
import openai
import os
from utils import save_conversation

app = FastAPI()

openai.api_key = os.getenv("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")

# Temporary in-memory store for conversation history per CallSid
conversation_history = {}

@app.post("/voice")
async def voice_webhook(request: Request):

    form = await request.form()
    user_input = form.get("SpeechResult")
    call_sid = form.get("CallSid") or "unknown"

    if not user_input:
        response = "<?xml version='1.0' encoding='UTF-8'?><Response><Say>Hi, this is Sofia from Legal Assist. I didn't hear anything. Can you please repeat that?</Say><Pause length='2'/><Redirect>/voice</Redirect></Response>"
        return PlainTextResponse(content=response, media_type="application/xml")

    # Initialize conversation history for new calls
    if call_sid not in conversation_history:
        conversation_history[call_sid] = [
            {"role": "system", "content": "You are Sofia, a friendly and professional assistant from Legal Assist. Your job is to conduct a personal injury claim intake call. Ask all required questions naturally, one at a time. Collect full name, accident date, type of accident, injuries, fault, and medical treatment. Also answer any user questions naturally like a human. End the call by saying a solicitor will call them shortly when done."}
        ]

    # Add user input to conversation history
    conversation_history[call_sid].append({"role": "user", "content": user_input})

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=conversation_history[call_sid]
        )
        ai_reply = completion.choices[0].message.content.strip()
        conversation_history[call_sid].append({"role": "assistant", "content": ai_reply})
    except Exception as e:
        ai_reply = "Sorry, I'm having trouble understanding right now. A solicitor will call you shortly."

    save_conversation(call_sid, user_input, ai_reply)

    # Check if Sofia should end the call
    if any(x in ai_reply.lower() for x in ["a solicitor will call you", "we will contact you", "thank you for your time"]):
        response = f"""
            <?xml version='1.0' encoding='UTF-8'?>
            <Response>
                <Say>{ai_reply}</Say>
                <Hangup/>
            </Response>
        """
    else:
        response = f"""
            <?xml version='1.0' encoding='UTF-8'?>
            <Response>
                <Say>{ai_reply}</Say>
                <Pause length='1'/>
                <Redirect>/voice</Redirect>
            </Response>
        """

    return PlainTextResponse(content=response.strip(), media_type="application/xml")
