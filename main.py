import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from typing import List
from pydantic import BaseModel
import httpx
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from bs4 import BeautifulSoup
from openai import OpenAI
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Setting(BaseModel):
    label: str
    type: str
    required: bool
    default: str


class MonitorPayload(BaseModel):
    channel_id: str
    return_url: str
    settings: List[Setting]


messages = {"657-098": ["this is how you make history! by being on time and doing your job well.", "Are you sure about that, Jason?", "Yes, I can guarantee that the server was working well last night.", "Remind me to take it up with management tomorroe morning, Sarah", "Yes, Chris. I will."]}


@app.get("/")
def read_root():
    return "Welcome to Couch Potato's Workspace 😁\n The integration is at this endpoint 👉🏼 baseurl/integration"

@app.get("/icon")
def get_icon():
    return FileResponse("homework.png", media_type="image/png")

@app.get("/integration")
def get_integration_json():
    return FileResponse("integration.json")

@app.post("/message-log")
async def get_message_log(request: Request):
    payload = await request.json()

    channel_id = payload["channel_id"]
    settings = payload["settings"]
    message = payload["message"]

    clean_message = BeautifulSoup(message, "html.parser").get_text()

    messages.append(channel_id[clean_message])
    return {
		"event_name": "message_logged",
        "message": message,
		"status":     "success",
		"username":   "daily-summarizer-bot",
	}

@app.post("/summary")
async def summarize(payload: MonitorPayload):

    channel_id = payload.channel_id

    summary_content, issues_detected = await summarize_messages(messages[channel_id])

    if issues_detected:
        troubleshooting = await generate_troubleshooting(issues_detected)
        response_message = f"{summary_content}\n\n{troubleshooting}"
    else:
        response_message = summary_content


    data = {
        "message": response_message,
        "username":   "daily-summarizer-bot",
        "event_name": "Daily Summary",
        "status": "success"
    }

    messages.clear()

    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)

def call_openai(prompt: str):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are an AI assistant."}, {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

async def summarize_messages(messages: List[str]):
    message = "\n".join(messages)
    prompt = f"Summarize the following messages:\n{message}\n\nAlso, identify any issues present in the messages."
    response = call_openai(prompt)

    if "Issues:" in response:
        summary, issues = response.split("Issues:")
    else:
        summary, issues = response, ""

    return summary.strip(), issues.strip()

async def generate_troubleshooting(issue_description: str):
    prompt = f"Provide troubleshooting steps for the following issue:\n{issue_description}"
    return call_openai(prompt)
