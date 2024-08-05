from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth, database

router = APIRouter()

@router.post("/movies/{movie_id}/comments", response_model=schemas.Comment)
def create_comment(movie_id: int, comment: schemas.CommentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_comment = models.Comment(text=comment.text, movie_id=movie_id, user_id=current_user.id, parent_id=comment.parent_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/movies/{movie_id}/comments", response_model=List[schemas.Comment])
def get_comments(movie_id: int, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()
    return comments

