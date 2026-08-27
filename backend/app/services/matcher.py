import re
from collections import Counter


def _tokens(text: str):
    return re.findall(r"[a-zA-Z0-9+#.]+", text.lower())


def compute_match_score(resume_text: str, job_description: str) -> float:
    resume_tokens = Counter(_tokens(resume_text))
    job_tokens = Counter(_tokens(job_description))

    if not job_tokens:
        return 0.0

    matched = sum(
        min(resume_tokens[word], count)
        for word, count in job_tokens.items()
        if word in resume_tokens
    )

    total = sum(job_tokens.values())

    return round((matched / total) * 100, 2)


def find_missing_skills(
    resume_skills: list,
    job_description: str,
    skill_keywords: list
) -> list:

    job_text = job_description.lower()

    required_skills = [
        skill
        for skill in skill_keywords
        if skill.lower() in job_text
    ]

    resume_skill_set = {
        skill.lower()
        for skill in resume_skills
    }

    return [
        skill
        for skill in required_skills
        if skill.lower() not in resume_skill_set
    ]
