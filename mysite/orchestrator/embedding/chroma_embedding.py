import json
import os
import pprint
from typing import List
import uuid
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

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
        self.chroma_client = chromadb.PersistentClient(path="chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="alchemist_collection_v1")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=50,
            length_function=len,
            is_separator_regex=False,
        )
        self.embeddings = OpenAIEmbeddings()

    def index_docs(self, docs: List[DocumentToIndex]): 
        for doc in docs:
            self.index_doc(doc)

    def index_doc(self, doc: DocumentToIndex): 
        doc_splits = self.text_splitter.create_documents([doc.text])
        pprint.pprint(f" docs: {doc_splits}")
        for split in doc_splits:
            pprint.pprint(split.page_content)
            generated_id = uuid.uuid4()
            embedding = self.embeddings.embed_text(split.page_content)
            self.collection.add(
                    documents = [split.page_content],
                    metadatas = [{"url": doc.url, "title": doc.title}],
                    ids = [str(generated_id)],
                    embeddings = [embedding]
                )

    def query_docs(self, query: str, n_results: int) -> List[str]:
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            # where={"metadata_field": "is_equal_to_this"}, # optional filter
            # where_document={"$contains":"search_string"}  # optional filter
        )
        return self._format_query_result(results)

    def _format_query_result(self, results: chromadb.QueryResult) -> List[str]:
        
        if(results is None):
            return []
        
        formatted_results = []
        result_documents = results.get("documents")
        for documents in result_documents:
            for document in documents:
                formatted_results.append(document)
                
        return formatted_results

if __name__ == "__main__":
    chroma_embedding = ChromaEmbedding()
    results = chroma_embedding.query_docs(
        query="Query about document spliting",
        n_results=2,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )
    pprint.pprint(results)
    #formatted = chroma_embedding._format_query_result(results)
    #pprint.pprint(formatted)