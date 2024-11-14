from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain.chains import create_retrieval_chain

from langchain_openai import ChatOpenAI

import os

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

class ChatWithDocumentView(View):
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, streaming= True)
        self.prompt = ChatPromptTemplate.from_template("""You are a world class question answering system and very good at summarizing doc.:
            <context>
            {context}
            </context>

            Question: {input}""")
        
        self.vector_store = Chroma(
            collection_name="alchemist_collection_v1",
            persist_directory="chroma_db",  # Where to save data locally, remove if not necessary
        )
        
    def post(self, request):
        data = json.loads(request.body)
        message = data.get('message')

        output_parser = StrOutputParser()
        
        document_chain = create_stuff_documents_chain(self.llm, prompt = self.prompt, output_parser=output_parser),
        retriever = self.vector_store.as_retriever(search_kwargs={'k': 3})
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        response = retrieval_chain.stream({"input": message})
        return JsonResponse({'response': response["answer"]})
