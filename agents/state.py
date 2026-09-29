from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    # add_messages ensures new messages append rather than overwrite
    messages: Annotated[list[BaseMessage], add_messages]
    query_plan: str
    error_state: bool