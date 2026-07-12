import streamlit as st
from pypdf import PdfReader

st.title("AI Resume Reviewer")

st.write("Upload your resume PDF and get AI-powered resume feedback.")

# Target role selection
target_role = st.selectbox(
    "Select your target role",
    [
        "Software Engineering Intern",
        "AI/ML Intern",
        "ECE Hardware Intern",
        "Embedded/Firmware Intern"
    ]
)

# Keyword lists for different roles
role_keywords = {
    "Software Engineering Intern": [
        "Python", "Java", "C++", "C", "Git", "Data Structures",
        "Algorithms", "Object-Oriented Programming", "Linux",
        "SQL", "REST API", "Debugging", "Software Development"
    ],
    "AI/ML Intern": [
        "Python", "Machine Learning", "Deep Learning", "TensorFlow",
        "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Data Analysis",
        "Model Training", "Neural Networks", "Generative AI", "LLM"
    ],
    "ECE Hardware Intern": [
        "C", "C++", "Verilog", "SystemVerilog", "FPGA", "Digital Design",
        "Circuit Design", "Oscilloscope", "PCB", "VHDL", "Signal Processing",
        "Embedded Systems", "Hardware Testing"
    ],
    "Embedded/Firmware Intern": [
        "C", "C++", "Embedded Systems", "Microcontroller", "RTOS",
        "Firmware", "SPI", "I2C", "UART", "ARM", "STM32",
        "Debugging", "Linux", "Hardware"
    ]
}

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

    st.subheader("ATS Keyword Analysis")

    selected_keywords = role_keywords[target_role]

    matched_keywords = []
    missing_keywords = []

    resume_text_lower = resume_text.lower()

    for keyword in selected_keywords:
        if keyword.lower() in resume_text_lower:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    score = round((len(matched_keywords) / len(selected_keywords)) * 100)

    st.metric("ATS Keyword Match Score", f"{score}%")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Matched Keywords")
        if matched_keywords:
            for keyword in matched_keywords:
                st.success(keyword)
        else:
            st.warning("No keywords matched.")

    with col2:
        st.write("### Missing Keywords")
        if missing_keywords:
            for keyword in missing_keywords:
                st.error(keyword)
        else:
            st.success("No missing keywords!")

    st.subheader("Basic Recommendation")

    if score >= 80:
        st.success("Your resume has strong keyword alignment for this role.")
    elif score >= 50:
        st.warning("Your resume has moderate keyword alignment. Consider adding more relevant technical keywords.")
    else:
        st.error("Your resume has low keyword alignment. You should tailor your resume more closely to this role.")