from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.models.candidate import Candidate
from app.services.ai_service import generate_questions

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/generate")
def generate_questions_api(candidate_id: str, role: str, db: Session = Depends(get_db)):

    candidate = db.query(Candidate).filter(
        Candidate.id == candidate_id
    ).first()

    if not candidate:
        return {"error": "Candidate not found"}

    questions = generate_questions(
        candidate.skills,
        candidate.projects,
        role
    )

    return {"questions": questions}