import os
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List, Dict, Any

CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")

# Initialize ChromaDB persistent client
client = chromadb.PersistentClient(path=CHROMA_PERSIST_DIRECTORY)

# Default embedding function used by Chroma is all-MiniLM-L6-v2
# We explicitly load it for clarity, though Chroma would do it by default.
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

COLLECTION_NAME = "tech_docs"

# Get or create collection
collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=sentence_transformer_ef
)

def add_documents(chunks: List[str], metadatas: List[Dict[str, Any]], ids: List[str]):
    """
    Adds chunks of text to the ChromaDB collection.
    """
    if not chunks:
        return
    collection.add(
        documents=chunks,
        metadatas=metadatas,
        ids=ids
    )

def query_documents(query_text: str, n_results: int = 4) -> List[str]:
    """
    Queries the vector store and returns the top matched document chunks.
    """
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Extract the documents
    if results['documents'] and len(results['documents']) > 0:
        return results['documents'][0]
    return []
