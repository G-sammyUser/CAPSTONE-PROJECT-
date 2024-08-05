from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth, database

router = APIRouter()

@router.post("/movies/{movie_id}/rate", response_model=schemas.Rating)
def rate_movie(movie_id: int, rating: schemas.RatingCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    db_rating = models.Rating(score=rating.score, movie_id=movie_id, user_id=current_user.id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/movies/{movie_id}/ratings", response_model=List[schemas.Rating])
def get_ratings(movie_id: int, db: Session = Depends(database.get_db)):
    ratings = db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()
    return ratings

