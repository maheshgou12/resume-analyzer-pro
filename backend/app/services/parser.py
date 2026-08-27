import re
from pathlib import Path
import pdfplumber
import docx
import spacy

nlp = spacy.load("en_core_web_sm")


def extract_text(file_path: str) -> str:
    path = Path(file_path)

    if path.suffix.lower() == ".pdf":
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
                text += "\n"
        return text

    elif path.suffix.lower() == ".docx":
        document = docx.Document(path)
        return "\n".join(
            paragraph.text for paragraph in document.paragraphs
        )

    else:
        raise ValueError("Unsupported file type. Use PDF or DOCX.")


def extract_entities(text: str):
    doc = nlp(text)

    entities = {
        "name": None,
        "email": None,
        "phone": None,
        "organizations": [],
        "skills": []
    }

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    if email_match:
        entities["email"] = email_match.group(0)

    phone_match = re.search(
        r"(?:\+91[-\s]?)?[6-9]\d{9}",
        text
    )

    if phone_match:
        entities["phone"] = phone_match.group(0)

    entities["organizations"] = [
        ent.text for ent in doc.ents
        if ent.label_ == "ORG"
    ]

    persons = [
        ent.text for ent in doc.ents
        if ent.label_ == "PERSON"
    ]

    if persons:
        entities["name"] = persons[0]

    skills = [
        "Python",
        "Java",
        "C",
        "C++",
        "SQL",
        "PostgreSQL",
        "MySQL",
        "FastAPI",
        "Django",
        "React",
        "JavaScript",
        "HTML",
        "CSS",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "Git",
        "GitHub"
    ]

    text_lower = text.lower()

    entities["skills"] = [
        skill for skill in skills
        if skill.lower() in text_lower
    ]

    return entities


def check_ats_formatting(file_path: str, text: str):
    issues = []
    score = 100

    if not text.strip():
        issues.append("No extractable text found")
        score -= 50

    if len(text) > 12000:
        issues.append("Resume may be too long")
        score -= 10

    if not re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    ):
        issues.append("Email address not found")
        score -= 10

    text_lower = text.lower()

    sections = [
        "experience",
        "education",
        "skills"
    ]

    for section in sections:
        if section not in text_lower:
            issues.append(f"Missing section: {section}")
            score -= 10

    return {
        "ats_score": max(score, 0),
        "issues": issues
    }

SKILL_KEYWORDS = [
    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "JavaScript",
    "HTML",
    "CSS",
    "React",
    "Node.js",
    "FastAPI",
    "Django",
    "Flask",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "TensorFlow",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "PostgreSQL",
    "MySQL",
    "MongoDB",
]
