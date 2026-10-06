import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document

load_dotenv()

# Initialize Google's Embedding Model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Initialize the local ChromaDB Vector Store
vector_store = Chroma(
    collection_name="postgres_docs",
    embedding_function=embeddings,
    persist_directory="./chroma_db"
)

def add_documents_to_db(docs):
    """Chunks and adds text documents to the vector database."""
    vector_store.add_documents(docs)
    return f"Successfully added {len(docs)} document chunks."

def search_postgres_docs(query: str, k: int = 3):
    """Searches the database for the most relevant context."""
    results = vector_store.similarity_search(query, k=k)
    return results