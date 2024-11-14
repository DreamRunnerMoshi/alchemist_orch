# views.py
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer

from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.6, streaming= True)

prompt = ChatPromptTemplate.from_template("""You are a world class question answering system and very good at summarizing doc.:
    <context>
    {context}
    </context>

    Question: {input}""")

vector_store = Chroma(
    collection_name="alchemist_collection_v1",
    persist_directory="chroma_db",  # Where to save data locally, remove if not necessary
)


@csrf_exempt
async def generate_chat_response(request):
    if request.method == 'POST':
        input_text = request.POST.get('messages', '')
        print(input_text)
        return JsonResponse({'response': "fsadfa"})
        response = await generate_response(input_text)
        # Generate response asynchronously
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
        # response = loop.run_until_complete(generate_response(input_text))

        return JsonResponse({'response': response})

async def generate_response(input_text):
    # Your ChatGPT processing logic here
    # You can use the Langchain library here to orchestrate the RAG system
    # This function should yield responses as they become available
    # Example:
    async for response_chunk in generate_chatgpt_response(input_text):
        channel_layer = get_channel_layer()
        await channel_layer.group_send(
            "chat_group",
            {
                "type": "chat_message",
                "message": response_chunk,
            }
        )

async def generate_chatgpt_response(input_text):
    # Your logic to generate responses from ChatGPT here
    # This function should yield response chunks as they become available
    # Example:
    prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
    parser = StrOutputParser()
    chain = prompt | llm | parser

    async for chunk in chain.astream({"topic": input_text}):
        print(chunk, end="|", flush=True)   
        yield chunk
