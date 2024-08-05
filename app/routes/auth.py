from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, database
from .utils import hash_password

router = APIRouter()

@router.post("/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    hashed_password = hash_password(user.password)
    # Add user to the database
    return {"message": "User registered successfully"}
