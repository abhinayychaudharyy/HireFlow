from sqlalchemy import Column, String, ForeignKey
from app.db.database import Base
import uuid

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    email = Column(String)
    resume = Column(String)  # Cloudinary URL
    job_id = Column(String, ForeignKey("jobs.id"))
    company_id = Column(String, ForeignKey("companies.id"))
