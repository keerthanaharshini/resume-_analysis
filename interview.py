import os
import streamlit as st
from google import genai

api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured")

client = genai.Client(api_key=api_key)

def generate_questions(resume_text):

    prompt = f"""
You are an experienced HR interviewer.

Candidate Resume:

{resume_text}

Generate exactly 5 technical interview questions based ONLY on the candidate's skills.

Rules:
1. Return only the questions.
2. Number them from 1 to 5.
3. Don't include answers.
"""

    # Retry 3 times
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            return response.text

        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(3)

    # Fallback questions
    return """1. Tell me about yourself.
2. Explain your final year project.
3. What is Object-Oriented Programming?
4. What are your strengths?
5. Why should we hire you?"""
