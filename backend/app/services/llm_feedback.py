import hashlib
import json

from groq import Groq
from app.config import settings


client = Groq(api_key=settings.GROQ_API_KEY)

_feedback_cache = {}


def generate_feedback(resume_text: str, job_description: str = "") -> dict:

    cache_input = resume_text + "||" + job_description

    cache_key = hashlib.sha256(
        cache_input.encode("utf-8")
    ).hexdigest()

    if cache_key in _feedback_cache:
        print("CACHE HIT")
        return _feedback_cache[cache_key]

    print("CACHE MISS - Calling Groq API")

    prompt = f"""
You are an expert resume reviewer and career coach.

Analyze the resume against the job description.

Return ONLY valid JSON.

Use exactly this structure:

{{
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "missing_skills": ["...", "..."],
  "suggestions": ["...", "..."]
}}

Resume:
{resume_text[:6000]}

Job Description:
{job_description[:2000]}
"""

   response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2,
    response_format={"type": "json_object"}
)

    content = response.choices[0].message.content.strip()

    if content.startswith("```json"):
        content = content[7:]

    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    try:
        result = json.loads(content)

    except json.JSONDecodeError:
        print("WARNING: Groq returned invalid JSON")

        result = {
            "strengths": [],
            "weaknesses": [],
            "missing_skills": [],
            "suggestions": [
                "LLM response could not be parsed."
            ]
        }

    _feedback_cache[cache_key] = result

    return result
