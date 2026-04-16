from pydantic import BaseModel, EmailStr

class CompanyBase(BaseModel):
    name: str
    email: EmailStr


class CompanyResponse(CompanyBase):
    id: str

    class Config:
        from_attributes = True