from typing import List
from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def call_ai(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are an AI assistant."}, {"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content.strip()

async def summarize_messages(messages: List[str]):
    message_text = "\n".join(messages)
    prompt = f"Summarize the following messages:\n{message_text}\n\nAlso, identify any issues present in the messages."
    response = call_ai(prompt)

    if "Issues:" in response:
        summary, issues = response.split("Issues:")
    else:
        summary, issues = response, ""

    return summary.strip(), issues.strip()

async def generate_troubleshooting(issue_description: str):
    prompt = f"Provide troubleshooting steps for the following issue:\n{issue_description}"
    return call_ai(prompt)
