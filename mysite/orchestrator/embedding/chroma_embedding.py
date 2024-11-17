import json
import os
import pprint
from typing import List, Tuple
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma

os.environ["OPENAI_API_KEY"] = 'sk-proj-zdiUmjsNs6PACoKSWrR2T3BlbkFJhOvMKIisyFJUdp2F13t3'

class DocumentToIndex:
    def __init__(self, title: str, text: str, url:str):
        self.title = title
        self.text = text
        self.url = url
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

class SearchResult:
    def __init__(self, title: str, url: str, text: str, id: str, distance: float):
        self.title = title
        self.url = url
        self.text = text
        self.id = id
        self.distance = distance
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
    
    def to_dict(self):
        return {
            'title': self.title,
            'url': self.url,
            'text': self.text,
            'id': self.id,
            'distance': self.distance
        }

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
        for split in doc_splits:
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
    
    def search_chroma(self, query: str, n_results: int) -> List[SearchResult]:
        results = self.vector_store.similarity_search_with_score(
            query=query,
            k=n_results
        )
        return self._format_query_result_with_score(results)

    def _format_query_result_with_score(self, results: List[Tuple[dict, float]]) -> List[SearchResult]:
        """
        Formats the query results with their respective scores into a list of SearchResult objects.
        Args:
            results (List[Tuple[dict, float]]): A list of tuples where each tuple contains a document (as a dictionary) 
                                                and a float representing the score.
        Returns:
            List[SearchResult]: A list of SearchResult objects with formatted query results.
        """
        if not results:
            return []
        formatted_results = []
        for item in results:

            doc, score = item

            title = doc.metadata["title"]
            url = doc.metadata["url"]

            formatted_results.append(
                SearchResult(
                    title=title,
                    url=url,
                    text=doc.page_content,
                    id=doc.id,
                    distance=score
                ))
                
        return formatted_results

    def _format_query_result(self, results: List[dict]) -> List[str]:
        if not results:
            return []
        
        formatted_results = []
        for res in results:
            formatted_results.append(res.page_content)
                
        return formatted_results

if __name__ == "__main__":
    chroma_embedding = ChromaEmbedding()
    results = chroma_embedding.search_chroma(
        query="Chroma is a text search engine",
        n_results=2,
    )
    for result in results:
        print(result.toJSON())