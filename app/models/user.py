from sqlalchemy import Column, String, ForeignKey
from app.db.database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="admin")
    company_id = Column(String, ForeignKey("companies.id"))