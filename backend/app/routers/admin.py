from collections import Counter

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, auth


router = APIRouter(prefix="/admin", tags=["admin"])


def get_admin_user(
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.is_admin != 1:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_admin_user)
):
    users = db.query(models.User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at
        }
        for user in users
    ]


@router.get("/analyses")
def get_all_analyses(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_admin_user)
):
    analyses = db.query(models.Analysis).order_by(
        models.Analysis.created_at.desc()
    ).all()

    return analyses


@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    admin: models.User = Depends(get_admin_user)
):
    analyses = db.query(models.Analysis).all()

    total = len(analyses)

    avg_match_score = (
        sum(a.match_score or 0 for a in analyses) / total
        if total > 0 else 0
    )

    avg_ats_score = (
        sum(a.ats_score or 0 for a in analyses) / total
        if total > 0 else 0
    )

    skill_counter = Counter()

    for analysis in analyses:
        for skill in (analysis.missing_skills or []):
            skill_counter[skill] += 1

    top_missing_skills = [
        {
            "skill": skill,
            "count": count
        }
        for skill, count in skill_counter.most_common(10)
    ]

    return {
        "total": total,
        "avg_match_score": round(avg_match_score, 2),
        "avg_ats_score": round(avg_ats_score, 2),
        "top_missing_skills": top_missing_skills
    }
