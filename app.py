import streamlit as st
import requests

# Page Configuration
st.set_page_config(
    page_title="DB-Doctor AI",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 DB-Doctor: PostgreSQL Optimization Agent")
st.markdown("Enter a SQL query below to run diagnostics, check execution plans, and receive AI-powered index recommendations using RAG.")

# Text input for the SQL query
sql_query = st.text_area(
    "SQL Query:",
    placeholder="SELECT * FROM users WHERE status = 'active';",
    height=100
)

if st.button("Diagnose Query", type="primary"):
    if not sql_query.strip():
        st.warning("Please enter a SQL query first.")
    else:
        with st.spinner("Analyzing execution plan and querying RAG database..."):
            try:
                # Send request to your FastAPI backend
                response = requests.post(
                    "http://localhost:8000/api/v1/agent/invoke",
                    json={"query": sql_query}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display results
                    st.success("Diagnostics Complete!")
                    
                    # Check if blocked by security
                    if data.get("error_blocked"):
                        st.error(f"Security Alert: {data.get('execution_plan')}")
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("📊 Execution Plan")
                            st.code(data.get("execution_plan"), language="text")
                        
                        with col2:
                            st.subheader("💡 DB-Doctor Recommendation")
                            # Extract text from the LLM response object list/dict
                            recommendations = data.get("recommendation", [])
                            if recommendations:
                                for rec in recommendations:
                                    st.markdown(rec.get("text", str(rec)))
                            else:
                                st.write("No specific recommendation generated.")
                else:
                    st.error(f"Server Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI backend. Make sure your `uvicorn` server is running!")