from fastapi import FastAPI
from app import models
from app.database import engine
from app.routes import auth, movies, ratings, comments

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(movies.router, prefix="/movies", tags=["movies"])
app.include_router(ratings.router, prefix="/ratings", tags=["ratings"])
app.include_router(comments.router, prefix="/comments", tags=["comments"])
