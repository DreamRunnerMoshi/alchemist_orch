
from dataclasses import dataclass
import json
import pprint
from typing import List

@dataclass
class ChatBotMessage:
    content: str
    """The contents of the system message."""
    role: str
    """The role of the messages author, in this case `system`."""

    def to_dict(self):
        return {
            "content": self.content,
            "role": self.role
        }

    @staticmethod
    def from_json(data: dict) -> 'ChatBotMessage':
        return ChatBotMessage(content=data['content'], role=data['role'])

@dataclass
class WebSocketPayload:
    type: str
    """The type of the message, in this case `websocket.receive`."""
    messages: List[ChatBotMessage]

    @staticmethod
    def from_json(json_data: dict) -> 'WebSocketPayload':
        payload = json.loads(json_data['text'])
        pprint.pprint(payload['messages'])
        user_conversations = [ChatBotMessage(**msg) for msg in payload.get('messages', [])]
        return WebSocketPayload(type=json_data['type'], messages=user_conversations)
