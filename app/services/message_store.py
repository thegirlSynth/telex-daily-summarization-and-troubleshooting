from collections import defaultdict
from typing import List

class MessageStore:
    def __init__(self):
        self.messages = defaultdict(list)

    def add_message(self, channel_id: str, message: str):
        self.messages[channel_id].append(message)

    def get_messages(self, channel_id: str) -> List[str]:
        return self.messages.get(channel_id, [])

    def clear_messages(self, channel_id: str):
        self.messages[channel_id] = []

message_store = MessageStore()
