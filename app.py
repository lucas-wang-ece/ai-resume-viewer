import streamlit as st
from pypdf import PdfReader
import re

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
        "C": [" c ", "c/", "/c", "c programming", "programming in c", "c/c++"],
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
        "C": [" c ", "c/", "/c", "c programming", "programming in c", "c/c++"],
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
        "C": [" c ", "c/", "/c", "c programming", "programming in c", "c/c++"],
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

action_verbs = [
    "develop", "developed",
    "implement", "implemented",
    "design", "designed",
    "build", "built",
    "create", "created",
    "optimize", "optimized",
    "debug", "debugged",
    "test", "tested",
    "analyze", "analyzed",
    "improve", "improved",
    "automate", "automated",
    "lead", "led",
    "manage", "managed",
    "collaborate", "collaborated",
    "engineer", "engineered",
    "integrate", "integrated",
    "configure", "configured",
    "deploy", "deployed",
    "maintain", "maintained",
    "program", "programmed",
    "simulate", "simulated",
    "monitor", "monitored",
    "update", "updated",
    "schedule", "scheduled",
    "teach", "taught",
    "foster", "fostered",
    "supervise", "supervised",
    "resolve", "resolved",
    "coordinate", "coordinated",
    "support", "supported",
    "assist", "assisted",
    "organize", "organized",
    "prepare", "prepared",
    "review", "reviewed",
    "research", "researched",
    "present", "presented"
]

technical_keywords = [
    "python",
    "java",
    "c++",
    "c/c++",
    "verilog",
    "systemverilog",
    "system verilog",
    "vhdl",
    "fpga",
    "git",
    "github",
    "linux",
    "api",
    "rest api",
    "sql",
    "pcb",
    "microcontroller",
    "embedded systems",
    "firmware",
    "machine learning",
    "neural network",
    "tensorflow",
    "pytorch",
    "numpy",
    "pandas",
    "algorithm",
    "algorithms",
    "data structures",
    "debugging",
    "debugged",
    "debug",
    "circuit design",
    "digital design",
    "digital logic",
    "oscilloscope",
    "signal processing",
    "hardware testing",
    "hardware design"
]

jd_keywords = {
    "Python": ["python"],
    "Java": ["java"],
    "C++": ["c++", "cpp"],
    "C": [" c ", "c/c++", "c programming"],
    "Git": ["git", "github"],
    "Linux": ["linux", "unix"],
    "SQL": ["sql", "mysql", "postgresql", "database"],
    "REST API": ["rest api", "api", "apis"],
    "Data Structures": ["data structures", "linked list", "stack", "queue", "tree", "hash table"],
    "Algorithms": ["algorithm", "algorithms"],
    "Object-Oriented Programming": ["object-oriented programming", "object oriented programming", "oop"],
    "Debugging": ["debug", "debugged", "debugging", "debugger"],
    "Software Development": ["software development", "developed", "implemented", "built"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Verilog": ["verilog"],
    "SystemVerilog": ["systemverilog", "system verilog"],
    "FPGA": ["fpga"],
    "Embedded Systems": ["embedded systems", "embedded"],
    "Firmware": ["firmware"],
    "Microcontroller": ["microcontroller", "microcontrollers", "mcu"],
    "PCB": ["pcb", "printed circuit board"],
    "Circuit Design": ["circuit design", "circuits"],
    "Digital Design": ["digital design", "digital logic"]
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


def extract_bullet_points(resume_text):
    lines = resume_text.split("\n")
    bullet_points = []

    for line in lines:
        clean_line = line.strip()

        if clean_line.startswith("•") or clean_line.startswith("-") or clean_line.startswith("*"):
            clean_line = clean_line.lstrip("•-* ").strip()
            if len(clean_line) > 10:
                bullet_points.append(clean_line)

    return bullet_points

def extract_keywords_from_job_description(job_description, keyword_dict):
    jd_text_lower = " " + job_description.lower() + " "
    jd_found_keywords = []

    for main_keyword, variations in keyword_dict.items():
        for variation in variations:
            if variation.lower() in jd_text_lower:
                jd_found_keywords.append(main_keyword)
                break

    return jd_found_keywords


def analyze_job_description_match(resume_text, job_description, keyword_dict):
    jd_found_keywords = extract_keywords_from_job_description(
        job_description,
        keyword_dict
    )

    resume_text_lower = " " + resume_text.lower() + " "

    matched_jd_keywords = []
    missing_jd_keywords = []

    for keyword in jd_found_keywords:
        variations = keyword_dict[keyword]
        found_in_resume = False

        for variation in variations:
            if variation.lower() in resume_text_lower:
                found_in_resume = True
                break

        if found_in_resume:
            matched_jd_keywords.append(keyword)
        else:
            missing_jd_keywords.append(keyword)

    if len(jd_found_keywords) == 0:
        jd_match_score = 0
    else:
        jd_match_score = round((len(matched_jd_keywords) / len(jd_found_keywords)) * 100)

    return jd_found_keywords, matched_jd_keywords, missing_jd_keywords, jd_match_score


def has_action_verb(bullet):
    words = bullet.strip().split()

    if not words:
        return False

    first_word = words[0].lower().strip(".,;:()[]")

    return first_word in action_verbs


def has_quantified_impact(bullet):
    return bool(re.search(r"\d+|%|\$|hours|users|students|projects|times", bullet.lower()))


def has_technical_keyword(bullet):
    bullet_lower = " " + bullet.lower() + " "

    for keyword in technical_keywords:
        if keyword in bullet_lower:
            return True

    return False

def analyze_bullet_points(bullet_points):
    results = []

    for bullet in bullet_points:
        action = has_action_verb(bullet)
        quantified = has_quantified_impact(bullet)
        technical = has_technical_keyword(bullet)

        score = 0
        if action:
            score += 1
        if quantified:
            score += 1
        if technical:
            score += 1

        results.append({
            "bullet": bullet,
            "action_verb": action,
            "quantified_impact": quantified,
            "technical_keyword": technical,
            "score": score
        })

    return results


uploaded_file = st.file_uploader("Upload your resume", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text")
    st.text_area("Resume Content", resume_text, height=300)

    st.subheader("Job Description Matching")

    job_description = st.text_area(
        "Paste a job description here to compare it with your resume",
        height=200
    )

    analyze_jd_button = st.button("Analyze Job Description Match")

    if analyze_jd_button:
        if not job_description.strip():
            st.warning("Please paste a job description before running the analysis.")
        else:
            jd_found_keywords, matched_jd_keywords, missing_jd_keywords, jd_match_score = analyze_job_description_match(
                resume_text,
                job_description,
                jd_keywords
            )

            st.metric("Job Description Match Score", f"{jd_match_score}%")

            st.write("### Keywords Found in Job Description")
            if jd_found_keywords:
                st.write(", ".join(jd_found_keywords))
            else:
                st.warning("No supported technical keywords were detected in the job description.")

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Matched JD Keywords")
                if matched_jd_keywords:
                    for keyword in matched_jd_keywords:
                        st.success(keyword)
                else:
                    st.warning("No JD keywords matched your resume.")

            with col2:
                st.write("### Missing JD Keywords")
                if missing_jd_keywords:
                    for keyword in missing_jd_keywords:
                        st.error(keyword)
                else:
                    st.success("No missing JD keywords!")

            if jd_match_score >= 80:
                st.success("Your resume has strong alignment with this job description.")
            elif jd_match_score >= 50:
                st.warning("Your resume has moderate alignment with this job description. Consider adding some missing JD keywords if they accurately reflect your experience.")
            else:
                st.error("Your resume has low alignment with this job description. Consider tailoring your resume more closely to the role.")

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

    st.subheader("Bullet Point Analysis")

    bullet_points = extract_bullet_points(resume_text)

    if not bullet_points:
        st.warning("No bullet points were detected. Make sure your resume uses bullet symbols such as • or -.")
    else:
        bullet_results = analyze_bullet_points(bullet_points)

        total_score = sum(result["score"] for result in bullet_results)
        max_score = len(bullet_results) * 3
        bullet_score = round((total_score / max_score) * 100)

        st.metric("Bullet Point Quality Score", f"{bullet_score}%")

        for index, result in enumerate(bullet_results, start=1):
            st.write(f"### Bullet {index}")
            st.write(result["bullet"])

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                if result["action_verb"]:
                    st.success("Action Verb")
                else:
                    st.error("No Action Verb")

            with col2:
                if result["quantified_impact"]:
                    st.success("Quantified")
                else:
                    st.warning("No Numbers")

            with col3:
                if result["technical_keyword"]:
                    st.success("Technical")
                else:
                    st.warning("No Tech Keyword")

            with col4:
                st.metric("Score", f"{result['score']}/3")

        st.subheader("Bullet Point Recommendation")

        if bullet_score >= 80:
            st.success("Your bullet points are strong. They include action verbs, technical details, and measurable impact.")
        elif bullet_score >= 50:
            st.warning("Your bullet points are decent, but some should include stronger action verbs, technical details, or measurable results.")
        else:
            st.error("Your bullet points need improvement. Try to start each bullet with an action verb and include measurable technical impact.")

        st.subheader("Overall Resume Score")

        overall_score = round((score * 0.5) + (bullet_score * 0.5))

        st.metric("Overall Resume Score", f"{overall_score}%")

        if overall_score >= 80:
            st.success(
                "Your resume is strong for this target role. It has solid keyword alignment and strong bullet point quality."
            )
        elif overall_score >= 60:
            st.warning(
                "Your resume is decent, but it could be improved by adding more relevant technical keywords and stronger measurable impact."
            )
        elif overall_score >= 40:
            st.warning(
                "Your resume needs improvement. Focus on adding missing role-specific keywords and quantifying your bullet point impact."
            )
        else:
            st.error(
                "Your resume currently has low alignment for this target role. Consider tailoring your resume with more technical keywords, stronger action verbs, and measurable results."
            )