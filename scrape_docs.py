import os
import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from agents.rag import add_documents_to_db

def scrape_postgres_docs():
    # Official PostgreSQL Performance Tips documentation page
    url = "https://www.postgresql.org/docs/current/performance-tips.html"
    
    print(f"Fetching documentation from {url}...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return

    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Target the main content area of the PostgreSQL documentation page
    content_div = soup.find('div', class_='sect1') or soup.find('div', class_='document')
    
    if content_div:
        text = content_div.get_text(separator="\n", strip=True)
    else:
        # Fallback to body text if specific class isn't found
        text = soup.get_text(separator="\n", strip=True)

    # Chunk the scraped text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_text(text)

    # Convert chunks to Document objects
    docs = [Document(page_content=chunk) for chunk in chunks]

    print(f"Extracted {len(docs)} chunks. Adding to ChromaDB...")
    result = add_documents_to_db(docs)
    print(result)

if __name__ == "__main__":
    scrape_postgres_docs()