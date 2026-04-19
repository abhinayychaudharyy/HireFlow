from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import auth, users
from app.api import jobs
from app.api import candidates
from app.api import questions

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
app.include_router(jobs.router, prefix="/jobs")
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")
app.include_router(questions.router)
@app.get("/")
def root():
    return {"message": "API running"}