from sqlalchemy import Column, String, ForeignKey,JSON
from app.db.database import Base
import uuid


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String) 
    job_id = Column(String, ForeignKey("jobs.id"))
    company_id = Column(String, ForeignKey("companies.id"))
    skills = Column(JSON, nullable=True)
    projects = Column(JSON, nullable=True)
    resume_url = Column(String)
