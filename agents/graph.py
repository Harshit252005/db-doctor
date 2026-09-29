import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

from agents.state import AgentState
from mcp_server import run_explain_plan

load_dotenv()

# Initialize Gemini as the reasoning engine
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# --- NODE 1: Run Database Diagnostics ---
def run_diagnostics_node(state: AgentState):
    """Takes the user's SQL query and runs the MCP diagnostic tool."""
    user_query = state["messages"][-1].content
    
    # Execute the MCP tool to get the execution plan
    plan_output = run_explain_plan(user_query)
    
    # Check if our security guardrail blocked the query
    if plan_output.startswith("ERROR:"):
        return {
            "query_plan": plan_output,
            "error_state": True,
            "messages": [AIMessage(content=f"Security Alert: {plan_output}")]
        }
    
    return {
        "query_plan": plan_output,
        "error_state": False
    }

# --- NODE 2: Generate Optimization Plan ---
def generate_optimization_node(state: AgentState):
    """Uses Gemini to analyze the execution plan and recommend fixes."""
    user_query = state["messages"][0].content
    execution_plan = state["query_plan"]
    
    system_prompt = (
        "You are DB-Doctor, a Senior Database Administrator. "
        "Analyze the user's SQL query and the provided database Execution Plan. "
        "1. Identify the exact bottleneck (e.g., Sequential Scan). "
        "2. Provide the exact SQL command to fix it (e.g., CREATE INDEX). "
        "3. Rewrite the query if needed. Keep it concise and technical."
    )
    
    prompt_messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"SQL Query: {user_query}\n\n{execution_plan}")
    ]
    
    response = llm.invoke(prompt_messages)
    return {"messages": [response]}

# --- ROUTER: Conditional Edge Logic ---
def check_security_router(state: AgentState) -> str:
    """Stops the agent immediately if a destructive query was blocked."""
    if state.get("error_state") is True:
        return "blocked"
    return "safe"

# --- BUILD THE GRAPH ---
workflow = StateGraph(AgentState)

# 1. Register the nodes
workflow.add_node("diagnostics", run_diagnostics_node)
workflow.add_node("optimizer", generate_optimization_node)

# 2. Connect the flow with edges
workflow.add_edge(START, "diagnostics")

# If safe -> go to optimizer. If blocked -> jump straight to END.
workflow.add_conditional_edges(
    "diagnostics",
    check_security_router,
    {
        "safe": "optimizer",
        "blocked": END
    }
)

workflow.add_edge("optimizer", END)

# 3. Compile into an executable application
db_doctor_graph = workflow.compile()