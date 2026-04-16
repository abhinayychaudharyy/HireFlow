from fastapi import FastAPI
from app.db.database import engine, Base
from app.api import auth, users
from app.api import jobs


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(jobs.router, prefix="/jobs")
app.include_router(auth.router, prefix="/auth")
app.include_router(users.router, prefix="/users")

@app.get("/")
def root():
    return {"message": "API running"}