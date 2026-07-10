import streamlit as st
from pypdf import PdfReader

st.title("AI Resume Reviewer")

st.write("Upload your resume PDF and get AI-powered feedback.")

uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")

    reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)