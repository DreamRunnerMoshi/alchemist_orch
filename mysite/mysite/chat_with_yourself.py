import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .llms.AlchemistGPT import AlchemistGPT

class ChatWithYourselfConsumer(AsyncWebsocketConsumer):
    
    def __init__(self):
        self.groups = [] 
        self.alchemist_gpt = AlchemistGPT()

    async def connect(self):
         # Initialize self.groups as an empty list
        await self.accept()
    
    async def disconnect(self, close_code):
        print(f"Disconnected {self.groups}")

    async def websocket_receive(self, text_data: str):
        #webSocketPayload = WebSocketPayload.from_json(text_data)
        #websocket payload whole data
        await self.stream_completions(text_data['text'])
        
    
    async def stream_completions(self, payload: any):
        data = json.loads(payload)
        message = data.get('messages')[-1].get('content')

        stream = await self.alchemist_gpt.astream(message)

        if stream is not None:
            async for chunk in stream:
                ans = chunk.get('answer')
                if ans is not None:
                    await self.send(text_data=ans)
        else:
            await self.send(text_data=json.dumps({"error": "Stream is None"}))
