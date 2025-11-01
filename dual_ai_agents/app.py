import streamlit as st
import pandas as pd
import os
import subprocess
from agents.test_case_agent import TestCaseAgent
from agents.sql_agent import SQLAgent

# Optional: lightweight Hugging Face model
from transformers import pipeline

# -------------------------------------------------
# Model Initialization
# -------------------------------------------------
def is_ollama_available():
    """Check if Ollama is installed and accessible."""
    try:
        subprocess.run(["ollama", "--version"], check=True, capture_output=True)
        return True
    except Exception:
        return False

def local_model(prompt: str) -> str:
    """
    Use Ollama if installed, otherwise fallback to a Hugging Face model.
    """
    if is_ollama_available():
        try:
            from ollama import chat
            result = chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            return result["message"]["content"]
        except Exception as e:
            return f"[Ollama Error] {e}"

    else:
        # Fallback: lightweight local model
        hf_model = pipeline("text-generation", model="facebook/bart-base", max_new_tokens=300)
        response = hf_model(prompt, truncation=True)[0]["generated_text"]
        return response

# -------------------------------------------------
# File Reader Helper
# -------------------------------------------------
def read_file_content(uploaded_file):
    """Read .txt, .csv, or .xlsx file and return text."""
    name = uploaded_file.name.lower()
    try:
        if name.endswith(".txt"):
            return uploaded_file.read().decode("utf-8", errors="ignore")
        elif name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            return df.to_string(index=False)
        elif name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
            return df.to_string(index=False)
        else:
            return "Unsupported file format."
    except Exception as e:
        return f"Error reading file: {e}"

# -------------------------------------------------
# Streamlit UI
# -------------------------------------------------
st.set_page_config(page_title="Dual AI Agents", page_icon="🧠", layout="wide")
st.title("🧠 Dual AI Agent System — Test Case & SQL Generator")

st.markdown("""
This app includes:
- **🧩 Test Case Agent** → Generates test cases from requirements  
- **🗃 SQL Agent** → Generates SQL from mapping documents  
Supports `.txt`, `.csv`, `.xlsx` uploads.  
Logs saved under `/logs/`.
""")

# Initialize agents
test_agent = TestCaseAgent(local_model)
sql_agent = SQLAgent(local_model)

tab1, tab2 = st.tabs(["🧩 Test Case Generator", "🗃 SQL Script Generator"])

# -------------------------------------------------
# TAB 1 — Test Case Generator
# -------------------------------------------------
with tab1:
    st.subheader("📄 Upload Requirements Document")
    uploaded_file = st.file_uploader("Upload .txt, .csv, or .xlsx file:", type=["txt", "csv", "xlsx"], key="req_upload")

    if uploaded_file:
        content = read_file_content(uploaded_file)
        st.text_area("📘 File Preview:", content[:2000], height=200)

        if st.button("🚀 Generate Test Cases"):
            with st.spinner("Generating test cases..."):
                result = test_agent.generate_test_cases(content)
                os.makedirs("outputs", exist_ok=True)
                with open("outputs/test_cases.txt", "w") as f:
                    f.write(result)
            st.success("✅ Test Cases Generated Successfully!")
            st.text_area("🧩 Generated Test Cases:", result, height=400)
            st.download_button("⬇️ Download Test Cases", result, file_name="test_cases.txt")

# -------------------------------------------------
# TAB 2 — SQL Script Generator
# -------------------------------------------------
with tab2:
    st.subheader("📊 Upload Mapping Document")
    uploaded_mapping = st.file_uploader("Upload .txt, .csv, or .xlsx file:", type=["txt", "csv", "xlsx"], key="map_upload")

    if uploaded_mapping:
        content = read_file_content(uploaded_mapping)
        st.text_area("📗 File Preview:", content[:2000], height=200)

        if st.button("🚀 Generate SQL Scripts"):
            with st.spinner("Generating SQL scripts..."):
                result = sql_agent.generate_sql(content)
                os.makedirs("outputs", exist_ok=True)
                with open("outputs/sql_scripts.sql", "w") as f:
                    f.write(result)
            st.success("✅ SQL Scripts Generated Successfully!")
            st.text_area("🗃 Generated SQL Scripts:", result, height=400)
            st.download_button("⬇️ Download SQL Scripts", result, file_name="sql_scripts.sql")

# -------------------------------------------------
# Sidebar Logs
# -------------------------------------------------
st.sidebar.title("📜 Agent Logs")

if os.path.exists("logs/test_agent.log"):
    with open("logs/test_agent.log") as f:
        st.sidebar.text_area("🧩 Test Agent Logs", f.read(), height=200)

if os.path.exists("logs/sql_agent.log"):
    with open("logs/sql_agent.log") as f:
        st.sidebar.text_area("🗃 SQL Agent Logs", f.read(), height=200)
