import pprint
import json
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_openai import ChatOpenAI
from channels.generic.websocket import AsyncWebsocketConsumer

import os

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

from langchain_community.embeddings import OpenAIEmbeddings

class ChatWithDocumentConsumer(AsyncWebsocketConsumer):
    
    def __init__(self):
        self.groups = [] 
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, streaming= True)
        self.prompt = ChatPromptTemplate.from_template("""You are a world class question answering system and very good at summarizing doc.:
            <context>
            {context}
            </context>

            Question: {input}""")
        
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            collection_name="alchemist_collection_v2",
            persist_directory="chroma_db",
            embedding_function=self.embeddings
        )

    async def connect(self):
         # Initialize self.groups as an empty list
        await self.accept()
    
    async def disconnect(self, close_code):
        pass

    async def websocket_receive(self, text_data: str):
        pprint.pprint(text_data)
        #webSocketPayload = WebSocketPayload.from_json(text_data)
        #websocket payload whole data
        await self.stream_completions(text_data['text'])
        
    
    async def stream_completions(self, payload: any):
        data = json.loads(payload)
        message = data.get('messages')[-1].get('content')

        output_parser = StrOutputParser()
        
        document_chain = create_stuff_documents_chain(self.llm, prompt = self.prompt, output_parser=output_parser)
        retriever = self.vector_store.as_retriever(search_kwargs={'k': 3})
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        stream = retrieval_chain.astream({"input": message})

        if stream is not None:
            async for chunk in stream:
                pprint.pprint(chunk)
                ans = chunk.get('answer')
                if ans is not None:
                    await self.send(text_data=ans)
        else:
            await self.send(text_data=json.dumps({"error": "Stream is None"}))
