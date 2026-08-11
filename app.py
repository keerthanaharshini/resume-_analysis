import streamlit as st
import pdfplumber

from resume_parser import analyze_resume
from interview import generate_questions
from evaluator import evaluate_answer

st.set_page_config(page_title="AI Resume Interview System", page_icon="📄")

st.title("📄 AI Resume Interview System")


st.header("👤 Candidate Information")

candidate_name = st.text_input("Candidate Name")

candidate_email = st.text_input("Email")

candidate_phone = st.text_input("Phone Number")

job_role = st.selectbox(
    "Job Role",
    [
        "Java Developer",
        "Python Developer",
        "Full Stack Developer",
        "Data Scientist",
        "AI Engineer",
        "Frontend Developer"
    ]
)

st.divider()




# --------------------------
# Session State
# --------------------------
if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

# --------------------------
# Upload Resume
# --------------------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# --------------------------
# Extract Resume Text
# --------------------------
def extract_text(file):
    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


# --------------------------
# Main Program
# --------------------------
if uploaded_file:

    resume_text = extract_text(uploaded_file)

    matched, missing, score = analyze_resume(resume_text)

    st.success("Resume Uploaded Successfully")

    st.subheader("Resume Score")
    st.progress(int(score))
    st.metric("Resume Score", f"{score}%")

    st.subheader("Skills Found")
    st.write(matched)

   # st.subheader("Missing Skills")
    #st.write(missing)

    # --------------------------
    # Generate Questions
    # --------------------------
    if st.button("🚀 Start Interview"):

        with st.spinner("Generating Questions..."):

            q = generate_questions(resume_text)

        st.session_state.questions = [
            line.strip()
            for line in q.split("\n")
            if line.strip()
        ]

        st.session_state.answers = []

    # --------------------------
    # Display Questions
    # --------------------------
    # --------------------------
# Display Questions
# --------------------------
if st.session_state.questions:

    st.header("🧠 AI Interview")

    # Clear old answers
    st.session_state.answers = []

    # Show all questions
    for i, question in enumerate(st.session_state.questions):

        st.subheader(question)

        answer = st.text_area(
            f"Your Answer {i+1}",
            key=f"answer_{i}"
        )

        st.session_state.answers.append(answer)

        # Submit Interview
    if st.button("Submit Interview"):

        total = 0

        # Evaluate all answers
        for i, question in enumerate(st.session_state.questions):

            answer = st.session_state[f"answer_{i}"]

            result = evaluate_answer(question, answer)

            # Extract score only
            try:
                score = int(result.split("Score:")[1].split("/")[0].strip())
                total += score
            except:
                pass

        # Final Result
        st.header("🎯 Interview Completed")

        st.metric("Final Interview Score", f"{total}/50")

        percentage = (total / 50) * 100

        st.progress(int(percentage))

        st.metric("Overall Percentage", f"{percentage:.2f}%")

        if percentage >= 80:
            st.success("⭐⭐⭐⭐⭐ Excellent")

        elif percentage >= 60:
            st.info("⭐⭐⭐⭐ Good")

        elif percentage >= 40:
            st.warning("⭐⭐⭐ Average")

        else:
            st.error("⭐⭐ Needs Improvement")