# 🩺 DB-Doctor: Autonomous PostgreSQL Diagnostics & Optimization Agent

[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-orange)](https://langchain-ai.github.io/langgraph/)
[![Google Gemini](https://img.shields.io/badge/Gemini-3.8--flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-red)](https://www.trychroma.com/)

**DB-Doctor** is an autonomous database optimization and diagnostics agent designed to bridge the gap between raw database metrics and actionable database administration. 

Built with **LangGraph**, **Model Context Protocol (MCP)**, **FastAPI**, and **Google Gemini**, DB-Doctor takes complex SQL queries, inspects live PostgreSQL query execution plans (`EXPLAIN ANALYZE`), retrieves official PostgreSQL tuning documentation via RAG, and produces deterministic, production-grade index recommendations and query rewrites.

---

## 📌 Architecture Overview

DB-Doctor models the database diagnostics workflow as a **Directed Acyclic Graph (DAG)** with deterministic state transitions and an automated security circuit-breaker:

```mermaid
graph TD
    START([User SQL Query]) --> Node1[Node 1: MCP Database Diagnostics]
    
    Node1 --> Router{Security Router: check_security_router}
    
    Router -- "Destructive Query (Blocked)" --> END([Fast Return: Security Alert])
    Router -- "Safe Read-Only Query" --> Node2[Node 2: Document Retrieval via ChromaDB]
    
    Node2 --> Node3[Node 3: Optimization Reasoning Engine with Gemini]
    Node3 --> END([Optimized SQL & Index Recommendations])

    classDef danger fill:#ff4d4f,stroke:#333,stroke-width:2px,color:#fff;
    classDef safe fill:#52c41a,stroke:#333,stroke-width:2px,color:#fff;
    classDef ai fill:#1890ff,stroke:#333,stroke-width:2px,color:#fff;

    class Router danger;
    class Node1,Node2 safe;
    class Node3 ai;
