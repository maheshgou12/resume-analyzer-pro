from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_admin: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class AnalysisOut(BaseModel):
    id: int
    match_score: float
    ats_score: float
    missing_skills: List[str]
    llm_feedback: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
