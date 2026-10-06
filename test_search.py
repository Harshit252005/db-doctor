from agents.rag import search_postgres_docs

# Simulate a user asking a vague question about database performance
user_question = "Why is my database reading every single row and slowing down? How do I fix it?"

# Ask ChromaDB to find the 1 most relevant chunk of context
results = search_postgres_docs(user_question, k=1)

print("Relevant context retrieved:\n")
print(f"'{results[0].page_content}'")