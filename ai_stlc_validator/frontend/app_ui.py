import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.title("🤖 AI STLC Validator")
st.markdown("Upload your **Mapping Document** and **Test Cases** to validate coverage automatically.")

mapping_file = st.file_uploader("📄 Upload Mapping Document (Excel)", type=["xlsx"])
testcase_file = st.file_uploader("🧪 Upload Test Case Document (Excel)", type=["xlsx"])

if st.button("Run Validation"):
    if mapping_file and testcase_file:
        files = {"mapping_file": mapping_file, "testcase_file": testcase_file}
        with st.spinner("Validating with AI..."):
            res = requests.post(f"{BACKEND_URL}/validate", files=files)
        if res.status_code == 200:
            st.success("✅ Validation complete!")
            report_path = res.json()["report_path"]
            st.download_button("⬇️ Download Validation Report", open(report_path, "rb"), file_name="validation_report.xlsx")
        else:
            st.error("❌ Validation failed.")
    else:
        st.warning("Please upload both files.")
