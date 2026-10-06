from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from agents.rag import add_documents_to_db

def load_data():
    # 1. Read the text file
    with open("postgres_data.txt", "r") as f:
        text = f.read()

    # 2. Split the text into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(text)

    # 3. Convert text chunks to Document objects
    docs = [Document(page_content=chunk) for chunk in chunks]

    # 4. Add them to the database
    print(f"Loaded {len(docs)} chunks. Embedding and saving to ChromaDB...")
    result = add_documents_to_db(docs)
    print(result)

if __name__ == "__main__":
    load_data()