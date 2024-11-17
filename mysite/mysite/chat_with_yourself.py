import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .models.data_models import WebSocketPayload

from orchestrator.llms.AlchemistGPT import AlchemistGPT

class ChatWithYourselfConsumer(AsyncWebsocketConsumer):
    
    def __init__(self):
        """
        self.groups is required for the websocket consumer to work
        self.alchemist_gpt is an instance of the AlchemistGPT class
        """
        self.groups = [] 
        self.alchemist_gpt = AlchemistGPT()

    async def connect(self):
        await self.accept()
    
    async def disconnect(self, close_code):
        print(f"Disconnected {self.groups}")

    async def websocket_receive(self, text_data: str):
        webSocketPayload = WebSocketPayload.from_json(text_data)
        lastMessage = webSocketPayload.messages[-1]
        await self.stream_completions(lastMessage.content)
        
    
    async def stream_completions(self, question: str):

        stream = await self.alchemist_gpt.astream(question)

        if stream is not None:
            async for chunk in stream:
                ans = chunk.get('answer')
                if ans is not None:
                    await self.send(text_data=ans)
        else:
            await self.send(text_data=json.dumps({"error": "Stream is None"}))
