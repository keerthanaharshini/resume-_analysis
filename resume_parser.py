# resume_parser.py

skills = [
    "python",
    "java",
    "c",
    "c++",
    "sql",
    "html",
    "css",
    "javascript",
    "react",
    "node.js",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "communication",
    "teamwork",
    "problem solving",
    "git",
    "github"
]

def analyze_resume(text):
    text = text.lower()

    matched = []

    for skill in skills:
        if skill in text:
            matched.append(skill)

    missing = list(set(skills) - set(matched))

    score = round((len(matched) / len(skills)) * 100, 2)

    return matched, missing, score