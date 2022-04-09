from sqlalchemy.orm import Session

from model import models
from schema import schemas


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def create_event(db: Session, event: schemas.EventBase):
    db_event = models.Event(title=event.title, sport_id=event.sport_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event
