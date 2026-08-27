from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def compute_match_score(resume_text: str, job_description: str) -> float:
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(job_description, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2).item()

    return round(float(score * 100), 2)

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

    missing = [
        skill
        for skill in required_skills
        if skill.lower() not in resume_skill_set
    ]

    return missing
