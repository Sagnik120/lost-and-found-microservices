from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.auth import mask_email

from app.database import SessionLocal, engine
from app import models
from app.auth import hash_password, verify_password
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth & User Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- DB Dependency ----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Schemas ----------
class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# ---------- Routes ----------
@app.post("/register")
def register_user(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User registered successfully"}

@app.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }

@app.get("/user/{user_id}/public")
def get_public_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    return {
        "name": user.name,
        "masked_email": mask_email(user.email)
    }

@app.get("/user/{user_id}")
def get_user_details(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return {"error": "User not found"}

    return {
        "name": user.name,
        "email": user.email
    }
