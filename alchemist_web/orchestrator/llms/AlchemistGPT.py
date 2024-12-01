import os
from dotenv import load_dotenv
from orchestrator.data_models.data_models import json_to_model
from orchestrator.embedding.chroma_embedding import ChromaEmbedding


from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from .model_providers import ModelProvider
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

"""
The AlchemistGPT class is designed to provide a question-answering and document summarization system using OpenAI's GPT-3.5-turbo model. 
It integrates with a Chroma-based embedding and vector store for document retrieval. The class initializes the language model, 
prompt template, embeddings, and vector store. It also includes an asynchronous method 'astream' that processes input messages 
by retrieving relevant documents and generating responses using a retrieval chain.
"""

class AlchemistGPT:
    def __init__(self):
        self.llm = ModelProvider().get_model()
        self.prompt = ChatPromptTemplate.from_template("""You are a world class question answering system and very good at summarizing doc.:
            <context>
            {context}
            </context>

            Question: {input}""")
        chroma = ChromaEmbedding()
        self.embeddings = chroma.embeddings
        self.vector_store = chroma.vector_store
        self.output_parser = StrOutputParser()

    async def astream(self, chat_session: dict):
        message = self._get_last_message(chat_session)
        # Create a document chain that processes documents using the language model and prompt
        document_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=self.prompt,
            output_parser=self.output_parser
        )
        # Set up the retriever to fetch relevant documents from the vector store
        retriever = self.vector_store.as_retriever(search_kwargs={'k': 3})
        
        # Create a retrieval chain that combines the retriever and document chain
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        # Process the input message through the retrieval chain and return the response
        return retrieval_chain.astream({"input": message})
    
    def _get_last_message(self, message_history) -> str:
        chat_session  = json_to_model(message_history)
        lastMessage = chat_session.messages[-1]
        return lastMessage.content