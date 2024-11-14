# consumers.py

import json
import pprint
from channels.generic.websocket import AsyncWebsocketConsumer
from openai import OpenAI
import os

from .models.chat_models import WebSocketPayload

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

class ChatGPTConsumer(AsyncWebsocketConsumer):

    client = OpenAI(
            organization='org-ROdsRxFwHq5KOHYVhreIGG25',
            project='proj_dyNIbzUJx56xiXHve8VY9P3A',
        )

    async def websocket_receive(self, text_data: str):
        pprint.pprint(text_data)
        #webSocketPayload = WebSocketPayload.from_json(text_data)
        #websocket payload whole data
        await self.stream_completions(text_data['text'])

    async def stream_completions(self, payload: any):

        payload = json.loads(payload)
        messages = payload.get('messages')
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages= messages,
            stream=True,
        )

        for chunk in stream:
            choice = chunk.choices[0]
            if choice.finish_reason!='stop' and choice.delta.content is not None:
                await self.send(text_data=chunk.choices[0].delta.content)
            else:
                await self.send(text_data='[DONE]')