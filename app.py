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
    value="SELECT * FROM users WHERE email = 'alex@example.com' ORDER BY created_at DESC;",
    height=100
)

if st.button("Diagnose Query", type="primary"):
    if not sql_query.strip():
        st.warning("Please enter a SQL query first.")
    else:
        with st.spinner("Analyzing execution plan and querying RAG database..."):
            try:
                # Send request to FastAPI backend
                response = requests.post(
                    "https://db-doctor-api.onrender.com", 
                    json={"query": sql_query},
                    timeout=60
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.success("Diagnostics Complete!")
                    
                    # Check if blocked by security
                    if data.get("error_blocked"):
                        st.error(f"Security Alert: {data.get('execution_plan')}")
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("📊 Execution Plan")
                            st.code(data.get("execution_plan", "No plan returned"), language="text")
                        
                        with col2:
                            st.subheader("💡 DB-Doctor Recommendation")
                            # Handle string or dict/list responses gracefully
                            rec_text = data.get("response") or data.get("recommendation")
                            if isinstance(rec_text, list):
                                for item in rec_text:
                                    st.markdown(item.get("text", str(item)) if isinstance(item, dict) else str(item))
                            elif rec_text:
                                st.markdown(str(rec_text))
                            else:
                                st.write("No specific recommendation generated.")
                else:
                    st.error(f"Server Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the FastAPI backend. Make sure your `uvicorn` server is running!")
            except requests.exceptions.Timeout:
                st.error("Request timed out waiting for the database and Gemini API.")