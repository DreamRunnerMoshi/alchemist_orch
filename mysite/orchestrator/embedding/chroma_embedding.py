import sys
import json
from typing import List
import uuid
import chromadb

class DocumentToIndex:
    def __init__(self, title: str, text: str, url:str):
        self.title = title
        self.text = text
        self.url = url
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


chroma_client = chromadb.PersistentClient(path="chroma_db")

collection = chroma_client.get_or_create_collection(name="alchemist_collection_v1")

def index_docs(docs: List[DocumentToIndex]): 

    for doc in docs:
        index_doc(doc)

def index_doc(doc: DocumentToIndex): 

    generated_id = uuid.uuid4()
    collection.add(
        documents = [doc.text],
        metadatas = [{"url": doc.url, "title": doc.title}],
        ids = [str(generated_id)]
    )

def search_docs(query: str):
    return collection.search(query)

if __name__ == "__main__":
    
    results = collection.query(
        query_texts=["Query about chromadb"],
        n_results=2,
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )
    print(results)