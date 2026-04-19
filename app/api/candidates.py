from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import os
import uuid
import shutil
from app.dependencies.db import get_db
from app.dependencies.auth import get_current_user
from app.models.candidate import Candidate
from app.services.upload_service import upload_resume
from app.services.resume_parser import parse_resume

router = APIRouter()


@router.post("/")
def add_candidate(
    name: str,
    email: str,
    job_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    temp_path = f"temp_{uuid.uuid4()}_{file.filename}"
    
    try:
        # 1. Save file locally for parsing
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2. Parse resume locally (Guarantees skills/projects capture even if Cloudinary has 401s)
        parsed_data = parse_resume(temp_path)

        # 3. Upload to Cloudinary (for storage and URL)
        # Re-open the local file for uploading
        with open(temp_path, "rb") as f:
            file_url = upload_resume(f, filename=file.filename)

        # 4. Save candidate in DB with all data in one go
        candidate = Candidate(
            name=name,
            email=email,
            resume_url=file_url,
            job_id=job_id.strip('"'),
            company_id=current_user.company_id,
            skills=parsed_data.get("skills"),
            projects=parsed_data.get("projects")
        )

        db.add(candidate)
        db.commit()
        db.refresh(candidate)

        return candidate

    except Exception as e:
        if db:
            db.rollback()
        print(f"ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process candidate: {str(e)}")

    finally:
        # 5. Cleanup local file
        if os.path.exists(temp_path):
            os.remove(temp_path)