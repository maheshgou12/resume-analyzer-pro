from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import shutil

from app.database import get_db
from app import models, schemas, auth
from app.services import parser, matcher, llm_feedback, report

router = APIRouter(prefix="/resumes", tags=["resumes"])

UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


@router.post("/analyze", response_model=schemas.AnalysisOut)
def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(""),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    text = parser.extract_text(file_path)
    entities = parser.extract_entities(text)
    ats = parser.check_ats_formatting(file_path, text)

    match_score = matcher.compute_match_score(
        text,
        job_description
    )

    missing = matcher.find_missing_skills(
        entities["skills"],
        job_description,
        parser.SKILL_KEYWORDS
    )

    feedback = llm_feedback.generate_feedback(
        text,
        job_description
    )

    resume = models.Resume(
        owner_id=current_user.id,
        filename=file.filename,
        raw_text=text,
        parsed_data=entities
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    analysis = models.Analysis(
        resume_id=resume.id,
        job_description=job_description,
        match_score=match_score,
        ats_score=ats["ats_score"],
        missing_skills=missing,
        llm_feedback=feedback
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    report_path = os.path.join(
        REPORT_DIR,
        f"analysis_{analysis.id}.pdf"
    )

    report.generate_report(
        output_path=report_path,
        filename=file.filename,
        match_score=match_score,
        ats_score=ats["ats_score"],
        missing_skills=missing,
        llm_feedback=feedback
    )

    return analysis


@router.get("/history", response_model=list[schemas.AnalysisOut])
def get_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    resumes = db.query(models.Resume).filter(
        models.Resume.owner_id == current_user.id
    ).all()

    resume_ids = [r.id for r in resumes]

    return db.query(models.Analysis).filter(
        models.Analysis.resume_id.in_(resume_ids)
    ).order_by(
        models.Analysis.created_at.desc()
    ).all()


@router.get("/report/{analysis_id}")
def download_report(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    analysis = db.query(models.Analysis).filter(
        models.Analysis.id == analysis_id
    ).first()

    if not analysis:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    resume = db.query(models.Resume).filter(
        models.Resume.id == analysis.resume_id,
        models.Resume.owner_id == current_user.id
    ).first()

    if not resume:
        raise HTTPException(
            status_code=404,
            detail="Analysis not found"
        )

    report_path = os.path.join(
        REPORT_DIR,
        f"analysis_{analysis.id}.pdf"
    )

    if not os.path.exists(report_path):
        report.generate_report(
            output_path=report_path,
            filename=resume.filename,
            match_score=analysis.match_score,
            ats_score=analysis.ats_score,
            missing_skills=analysis.missing_skills or [],
            llm_feedback=analysis.llm_feedback or {}
        )

    return FileResponse(
        report_path,
        media_type="application/pdf",
        filename=f"resume_analysis_{analysis.id}.pdf"
    )
