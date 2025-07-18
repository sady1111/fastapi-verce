from fastapi import FastAPI, Request, Form
from fastapi.responses import Response
import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "UK Personal Injury Bot Active - Legal Assist"}

@app.post("/call")
async def handle_call(request: Request):
    twiml = """
    <Response>
        <Gather input="speech" action="/step1" method="POST">
            <Say>Hello, this is Sofia calling from Legal Assist regarding a personal injury claim. May I know if you've had any accident in the last 6 months?</Say>
        </Gather>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")

@app.post("/step1")
async def step1(request: Request):
    data = await request.form()
    speech = data.get("SpeechResult", "").lower()

    if "yes" in speech:
        response = """
        <Response>
            <Gather input="speech" action="/step2" method="POST">
                <Say>Can you briefly tell me what kind of accident it was? For example, was it a road traffic accident, accident at work, or a public place incident?</Say>
            </Gather>
        </Response>
        """
    else:
        response = """
        <Response>
            <Say>Alright, thank you for your time. If anything happens in the future, feel free to reach out to Legal Assist. Goodbye.</Say>
            <Hangup/>
        </Response>
        """
    return Response(content=response.strip(), media_type="application/xml")

@app.post("/step2")
async def step2(request: Request):
    data = await request.form()
    speech = data.get("SpeechResult", "").lower()

    if any(x in speech for x in ["road", "car", "traffic", "vehicle"]):
        category = "Road Traffic Accident"
    elif "work" in speech:
        category = "Accident at Work"
    elif "public" in speech:
        category = "Public Place Accident"
    else:
        category = "Other"

    response = f"""
    <Response>
        <Gather input="speech" action="/step3" method="POST">
            <Say>Thank you. You mentioned a {category}. Can you please confirm the approximate date of the accident?</Say>
        </Gather>
    </Response>
    """
    return Response(content=response.strip(), media_type="application/xml")

@app.post("/step3")
async def step3(request: Request):
    data = await request.form()
    speech = data.get("SpeechResult", "").lower()

    try:
        today = datetime.date(2025, 8, 1)
        accident_date = datetime.datetime.strptime(speech, "%d %B %Y").date()
        six_months_ago = today - datetime.timedelta(days=183)

        if accident_date < six_months_ago or accident_date > today:
            return Response(content="""
            <Response>
                <Say>Unfortunately, we are only handling accidents that happened in the last 6 months before August 2025. Thank you and goodbye.</Say>
                <Hangup/>
            </Response>
            """.strip(), media_type="application/xml")
    except:
        return Response(content="""
        <Response>
            <Gather input="speech" action="/step3" method="POST">
                <Say>Sorry, I couldn't understand the date. Please say the accident date again, for example: Fifteenth May 2025.</Say>
            </Gather>
        </Response>
        """.strip(), media_type="application/xml")

    response = """
    <Response>
        <Gather input="speech" action="/step4" method="POST">
            <Say>Were you injured in the accident?</Say>
        </Gather>
    </Response>
    """
    return Response(content=response.strip(), media_type="application/xml")

@app.post("/step4")
async def step4(request: Request):
    data = await request.form()
    speech = data.get("SpeechResult", "").lower()

    if "no" in speech:
        return Response(content="""
        <Response>
            <Say>Unfortunately, we can only proceed with claims involving personal injury. Thank you for your time. Goodbye.</Say>
            <Hangup/>
        </Response>
        """.strip(), media_type="application/xml")

    response = """
    <Response>
        <Gather input="speech" action="/step5" method="POST">
            <Say>Were you the driver, passenger, pedestrian or a worker?</Say>
        </Gather>
    </Response>
    """
    return Response(content=response.strip(), media_type="application/xml")

@app.post("/step5")
async def step5(request: Request):
    response = """
    <Response>
        <Gather input="speech" action="/step6" method="POST">
            <Say>Do you know if the accident was someone else's fault?</Say>
        </Gather>
    </Response>
    """
    return Response(content=response.strip(), media_type="application/xml")

@app.post("/step6")
async def step6(request: Request):
    data = await request.form()
    speech = data.get("SpeechResult", "").lower()

    if "no" in speech or "not sure" in speech:
        return Response(content="""
        <Response>
            <Say>No worries, our legal team can still assess your claim. We will review your case and contact you soon. Thank you!</Say>
            <Hangup/>
        </Response>
        """.strip(), media_type="application/xml")

    response = """
    <Response>
        <Say>Perfect. Based on what you've told me, your case seems eligible. Our solicitors will call you shortly to proceed. Thank you and goodbye.</Say>
        <Hangup/>
    </Response>
    """
    return Response(content=response.strip(), media_type="application/xml")
