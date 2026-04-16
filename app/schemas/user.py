from pydantic import BaseModel, EmailStr

# Signup request
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


# Login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Response
class TokenResponse(BaseModel):
    access_token: str