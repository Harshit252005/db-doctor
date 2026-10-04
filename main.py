from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
import os

from agents.graph import db_doctor_graph

load_dotenv()

# This is the exact line your terminal was looking for!
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
def invoke_agent(request: QueryRequest):
    initial_state = {
        "messages": [HumanMessage(content=request.query)],
        "query_plan": "",
        "error_state": False
    }
    
    final_state = db_doctor_graph.invoke(initial_state)
    ai_response = final_state["messages"][-1].content
    
    return {
        "input_query": request.query,
        "execution_plan": final_state["query_plan"],
        "error_blocked": final_state["error_state"],
        "recommendation": ai_response
    }