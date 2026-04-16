from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.candidate import Candidate
from app.services.upload_service import upload_resume

router = APIRouter()


@router.post("/")
def add_candidate(
    name: str,
    email: str,
    job_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        #  Upload file to Cloudinary
        file_url = upload_resume(file.file)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    try:
        # Save candidate in DB
        candidate = Candidate(
            name=name,
            email=email,
            resume=file_url,
            job_id=job_id,
            company_id=current_user.company_id
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    except Exception as e:
        db.rollback()  # VERY IMPORTANT
        raise HTTPException(status_code=500, detail="Database error")

    return candidate