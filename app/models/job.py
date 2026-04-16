from sqlalchemy import Column, String, ForeignKey
from app.db.database import Base
import uuid

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String)
    description = Column(String)
    company_id = Column(String, ForeignKey("companies.id"))