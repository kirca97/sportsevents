from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import crud, models, schemas
from database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sports/", response_model=List[schemas.Sport])
def get_sports(db: Session = Depends(get_db)):
    sports = crud.get_sports(db)
    return sports


@app.post("/sports/", response_model=schemas.Sport)
def create_sport(sport: schemas.SportBase, db: Session = Depends(get_db)):
    db_sport = crud.get_sport_by_title(db, title=sport.title)
    if db_sport:
        raise HTTPException(status_code=400, detail="Sport already exists!")
    return crud.create_sport(db=db, sport=sport)
