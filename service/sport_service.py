from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import crud_sport
from schema import schemas


def get_sports(db: Session):
    return crud_sport.get_sports(db=db)


def get_sport_by_title(db: Session, title: str):
    return crud_sport.get_sport_by_title(db=db, title=title)


def get_sport_by_id(db: Session, id: int):
    return crud_sport.get_sport_by_id(db=db, id=id)


def create_sport(db: Session, sport: schemas.SportBase):
    db_sport = crud_sport.get_sport_by_title(db, title=sport.title)
    if db_sport:
        raise HTTPException(status_code=400, detail="Sport already exists!")
    return crud_sport.create_sport(db=db, sport=sport)
