from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.models.user import User
from app.models.company import Company
from app.core.security import hash_password, verify_password, create_token
from app.schemas.user import SignupRequest, LoginRequest

router = APIRouter()

@router.post("/signup")
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    company = Company(name=data.name, email=data.email)
    db.add(company)
    db.commit()
    db.refresh(company)

    user = User(
        email=data.email,
        password=hash_password(data.password),
        role="admin",
        company_id=company.id
    )
    db.add(user)
    db.commit()

    token = create_token({
        "user_id": user.id,
        "company_id": company.id
    })

    return {
    "access_token": token,
    "company": {
        "id": company.id,
        "name": company.name,
        "email": company.email
    }
}


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Wrong password")

    token = create_token({
        "user_id": user.id,
        "company_id": user.company_id
    })
    
    return {"access_token": token}