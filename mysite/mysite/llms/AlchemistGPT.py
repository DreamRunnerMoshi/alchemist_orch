import os
from dotenv import load_dotenv
from orchestrator.embedding.chroma_embedding import ChromaEmbedding


from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

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
        self.llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.3, streaming=True)
        self.prompt = ChatPromptTemplate.from_template("""You are a world class question answering system and very good at summarizing doc.:
            <context>
            {context}
            </context>

            Question: {input}""")
        chroma = ChromaEmbedding()
        self.embeddings = chroma.embeddings
        self.vector_store = chroma.vector_store

    async def astream(self, message):
        output_parser = StrOutputParser()
        document_chain = create_stuff_documents_chain(self.llm, prompt=self.prompt, output_parser=output_parser)
        retriever = self.vector_store.as_retriever(search_kwargs={'k': 3})
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        return retrieval_chain.astream({"input": message})