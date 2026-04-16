from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.job import Job
from app.schemas.job import JobCreate

router = APIRouter()


@router.post("/")
def create_job(
    data: JobCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    job = Job(
        title=data.title,
        description=data.description,
        company_id=current_user.company_id
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@router.get("/")
def get_jobs(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    jobs = db.query(Job).filter(
        Job.company_id == current_user.company_id
    ).all()

    return jobs