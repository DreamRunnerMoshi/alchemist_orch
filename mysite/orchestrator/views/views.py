from django.http import HttpResponse
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.embeddings import OllamaEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import WebBaseLoader

vector = None

def __init__(self):
    loader = WebBaseLoader("https://docs.smith.langchain.com/user_guide")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)

embeddings = OllamaEmbeddings()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class technical documentation writer."),
    ("user", "{input}")
])

llm = Ollama(model="llama2")
output_parser = StrOutputParser()


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message')
        
        # Here you would process the message, interact with your language model, and get a response
        # For demonstration purposes, let's just echo the message
        # response = f"You said: {message}"
        chain = prompt | llm | output_parser
        response = chain.invoke(message)
        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)