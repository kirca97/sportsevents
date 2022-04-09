from sqlalchemy.orm import Session

from . import models, schemas


def get_sports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sport).offset(skip).limit(limit).all()


def get_sport_by_title(db: Session, title: str):
    return db.query(models.Sport).filter(models.Sport.title == title).first()


def create_sport(db: Session, sport: schemas.SportBase):
    db_sport = models.Sport(title=sport.title)
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)
    return db_sport
