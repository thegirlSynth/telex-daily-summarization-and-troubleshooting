from fastapi import APIRouter
import httpx
from app.models import MonitorPayload
from app.services.message_store import message_store
from app.services.ai_service import summarize_messages, generate_troubleshooting

router = APIRouter()

@router.post("/summary")
async def summarize(payload: MonitorPayload):
    channel_id = payload.channel_id

    messages = message_store.get_messages(channel_id)
    if not messages:
        return {"status": "error", "message": "No messages to summarize."}

    summary_content, issues_detected = await summarize_messages(messages)

    if issues_detected:
        troubleshooting = await generate_troubleshooting(issues_detected)
        response_message = f"{summary_content}\n\n{troubleshooting}"
    else:
        response_message = summary_content

    data = {
        "message": response_message,
        "username": "daily-summarizer-bot",
        "event_name": "Daily Summary",
        "status": "success",
    }

    message_store.clear_messages(channel_id)

    async with httpx.AsyncClient() as client:
        await client.post(payload.return_url, json=data)

    return {"status": "success", "message": "Summary sent."}
