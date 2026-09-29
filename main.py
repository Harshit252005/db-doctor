from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="DB-Doctor Agent API", version="1.0.0")

class QueryRequest(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "api_key_loaded": bool(os.getenv("GOOGLE_API_KEY"))
    }

@app.post("/api/v1/agent/invoke")
async def invoke_agent(request: QueryRequest):
    # Tomorrow we will wire this endpoint to trigger the LangGraph agent
    return {"message": "Request received! Agent routing coming next.", "input": request.query}