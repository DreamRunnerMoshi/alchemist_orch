
from dataclasses import dataclass
import json
import pprint
from typing import Dict, List

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



from dataclasses import dataclass, field
from typing import List
import uuid


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ChatSession:
    uuid: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "chatboxai-3.5"
    messages: List[Message] = field(default_factory=list)
    temperature: float = 0.7
    language: str = "en"
    stream: bool = True

    def add_message(self, role: str, content: str):
        """Helper method to add a message to the session."""
        self.messages.append(Message(role=role, content=content))\
        
def json_to_model(json_data: Dict) -> ChatSession:
    """Converts JSON data into a ChatSession model."""
    messages = [
        Message(role=msg["role"], content=msg["content"])
        for msg in json_data.get("messages", [])
    ]
    
    return ChatSession(
        uuid=json_data.get("uuid", str(uuid.uuid4())),
        model=json_data.get("model", "chatboxai-3.5"),
        messages=messages,
        temperature=json_data.get("temperature", 0.7),
        language=json_data.get("language", "en"),
        stream=json_data.get("stream", True),
    )