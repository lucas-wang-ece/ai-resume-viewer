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

# Keyword dictionary with synonyms and variations
role_keywords = {
    "Software Engineering Intern": {
        "Python": ["python"],
        "Java": ["java"],
        "C++": ["c++", "cpp"],
        "C": [" c ", "c programming", "programming in c"],
        "Git": ["git", "github"],
        "Data Structures": ["data structures", "linked list", "tree", "stack", "queue", "hash table"],
        "Algorithms": ["algorithms", "algorithm"],
        "Object-Oriented Programming": ["object-oriented programming", "object oriented programming", "oop"],
        "Linux": ["linux", "unix"],
        "SQL": ["sql", "mysql", "postgresql", "database"],
        "REST API": ["rest api", "api", "apis"],
        "Debugging": ["debugging", "debugged", "debug", "debugger"],
        "Software Development": ["software development", "developed", "implemented", "built"]
    },
    "AI/ML Intern": {
        "Python": ["python"],
        "Machine Learning": ["machine learning", "ml"],
        "Deep Learning": ["deep learning"],
        "TensorFlow": ["tensorflow"],
        "PyTorch": ["pytorch"],
        "Pandas": ["pandas"],
        "NumPy": ["numpy"],
        "Scikit-learn": ["scikit-learn", "sklearn"],
        "Data Analysis": ["data analysis", "analyzed data", "data analytics"],
        "Model Training": ["model training", "trained model", "training models"],
        "Neural Networks": ["neural network", "neural networks"],
        "Generative AI": ["generative ai", "genai"],
        "LLM": ["llm", "large language model", "large language models"]
    },
    "ECE Hardware Intern": {
        "C": [" c ", "c/", "/c", "c programming", "programming in c", " c/c++", "c/c++"],
        "C++": ["c++", "cpp"],
        "Verilog": ["verilog"],
        "SystemVerilog": ["systemverilog", "system verilog"],
        "FPGA": ["fpga"],
        "Digital Design": ["digital design", "digital logic"],
        "Circuit Design": ["circuit design", "circuits"],
        "Oscilloscope": ["oscilloscope"],
        "PCB": ["pcb", "printed circuit board"],
        "VHDL": ["vhdl"],
        "Signal Processing": ["signal processing"],
        "Embedded Systems": ["embedded systems", "embedded"],
        "Hardware Testing": ["hardware testing", "tested hardware", "hardware design"]
    },
    "Embedded/Firmware Intern": {
        "C": [" c ", "c programming", "programming in c"],
        "C++": ["c++", "cpp"],
        "Embedded Systems": ["embedded systems", "embedded"],
        "Microcontroller": ["microcontroller", "microcontrollers", "mcu"],
        "RTOS": ["rtos", "real-time operating system"],
        "Firmware": ["firmware"],
        "SPI": ["spi"],
        "I2C": ["i2c"],
        "UART": ["uart"],
        "ARM": ["arm"],
        "STM32": ["stm32"],
        "Debugging": ["debugging", "debugged", "debug", "debugger"],
        "Linux": ["linux"],
        "Hardware": ["hardware", "hardware design", "hardware testing"]
    }
}


def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

    return resume_text


def analyze_keywords(resume_text, keyword_dict):
    resume_text_lower = " " + resume_text.lower() + " "

    matched_keywords = []
    missing_keywords = []

    for main_keyword, variations in keyword_dict.items():
        found = False

        for variation in variations:
            if variation.lower() in resume_text_lower:
                found = True
                break

        if found:
            matched_keywords.append(main_keyword)
        else:
            missing_keywords.append(main_keyword)

    score = round((len(matched_keywords) / len(keyword_dict)) * 100)

    return matched_keywords, missing_keywords, score


uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)

    st.subheader("ATS Keyword Analysis")

    selected_keywords = role_keywords[target_role]

    matched_keywords, missing_keywords, score = analyze_keywords(
        resume_text,
        selected_keywords
    )

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