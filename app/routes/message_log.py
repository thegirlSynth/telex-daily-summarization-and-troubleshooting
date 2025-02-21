from fastapi import APIRouter, Request
from bs4 import BeautifulSoup
from app.services.message_store import message_store

router = APIRouter()

@router.post("/message-log")
async def get_message_log(request: Request):
    payload = await request.json()

    channel_id = payload["channel_id"]
    message = payload["message"]

    clean_message = BeautifulSoup(message, "html.parser").get_text()

    message_store.add_message(channel_id, clean_message)

    return {
        "event_name": "message_logged",
        "message": message,
        "status": "success",
        "username": "daily-summarizer-bot",
    }
