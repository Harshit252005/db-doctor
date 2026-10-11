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
    value="SELECT * FROM users WHERE status = 'active' ORDER BY created_at DESC;",
    height=100
)

# Base Render API URL
API_BASE_URL = "https://db-doctor-api.onrender.com"

if st.button("Diagnose Query", type="primary"):
    if not sql_query.strip():
        st.warning("Please enter a SQL query first.")
    else:
        with st.spinner("Analyzing execution plan and querying RAG database..."):
            try:
                # Target the /diagnose route
                target_url = f"{API_BASE_URL}/diagnose"
                response = requests.post(
                    target_url, 
                    json={"query": sql_query},
                    timeout=90
                )
                
                # Fallback check in case the endpoint was mapped to /api/v1/agent/invoke or /
                if response.status_code == 404:
                    fallback_url = f"{API_BASE_URL}/api/v1/agent/invoke"
                    response = requests.post(
                        fallback_url,
                        json={"query": sql_query},
                        timeout=90
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
                st.error("Could not connect to the FastAPI backend. Make sure your Render instance is active!")
            except requests.exceptions.Timeout:
                st.error("Request timed out. If Render's free tier was asleep, it may take 50 seconds to warm up—please retry.")