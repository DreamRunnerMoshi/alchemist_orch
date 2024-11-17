import json
import os
import pprint
from typing import List
import uuid
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

class DocumentToIndex:
    def __init__(self, title: str, text: str, url:str):
        self.title = title
        self.text = text
        self.url = url
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class ChromaEmbedding:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large",
            # With the `text-embedding-3` class
            # of models, you can specify the size
            # of the embeddings you want returned.
            # dimensions=1024
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        persistent_client = chromadb.PersistentClient()
        self.vector_store = Chroma(
            client=persistent_client,
            collection_name="alchemist_collection_v2",
            embedding_function=self.embeddings,
            persist_directory="chroma_db"
        )

    def index_docs(self, docs: List[DocumentToIndex]): 
        for doc in docs:
            self.index_doc(doc)

    def index_doc(self, doc: DocumentToIndex): 
        doc_splits = self.text_splitter.create_documents([doc.text])
        pprint.pprint(f" docs: {doc_splits}")
        for split in doc_splits:
            pprint.pprint(split.page_content)
            self.vector_store.add_texts(
                texts=[split.page_content],
                metadatas=[{"url": doc.url, "title": doc.title}]
            )

    def query_docs(self, query: str, n_results: int) -> List[str]:
        results = self.vector_store.similarity_search(
            query=query,
            k=n_results
        )
        return self._format_query_result(results)

    def _format_query_result(self, results: List[dict]) -> List[str]:
        if not results:
            return []
        
        formatted_results = []
        for res in results:
            formatted_results.append(res.page_content)
            print(f"* {res.page_content} [{res.metadata}]")
                
        return formatted_results

if __name__ == "__main__":
    chroma_embedding = ChromaEmbedding()
    results = chroma_embedding.query_docs(
        query="test",
        n_results=2,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )
    pprint.pprint(results)
    #formatted = chroma_embedding._format_query_result(results)
    #pprint.pprint(formatted)