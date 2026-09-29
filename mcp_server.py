import asyncio
from mcp.server.fastmcp import FastMCP

# Create a local FastMCP server instance
mcp = FastMCP(name="DB-Doctor Diagnostic Server")

@mcp.tool
def run_explain_plan(query: str) -> str:
    """
    Simulates running an EXPLAIN ANALYZE on a database query.
    Takes a raw SQL query and returns the execution plan.
    """
    # Guardrail: Prevent destructive commands
    forbidden_keywords = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER"]
    if any(keyword in query.upper() for keyword in forbidden_keywords):
        return "ERROR: Destructive operations are blocked by security guardrails."
    
    # In a real app, you would connect to PostgreSQL/MongoDB here.
    # For now, we return a mock execution plan for the AI to analyze.
    return f"Execution Plan for '{query}':\n- Seq Scan on users (cost=0.00..25.00 rows=1000)\n- Missing Index on 'email' column detected."

@mcp.tool
def inspect_schema(table_name: str) -> str:
    """Returns the database schema for a given table."""
    return f"Schema for {table_name}: \n- id: UUID (Primary Key)\n- email: VARCHAR (No Index)\n- created_at: TIMESTAMP"

if __name__ == "__main__":
    # Runs the server locally
    mcp.run()