from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import crud_event, crud_sport
from schema import schemas


def get_events(db: Session):
    events = crud_event.get_events(db=db)
    return [schemas.EventDTO(id=event.id, title=event.title, sport_name=event.sport.title) for event in events]


def create_event(db: Session, event: schemas.EventBase):
    db_sport = crud_sport.get_sport_by_id(db=db, id=event.sport_id)
    if not db_sport:
        raise HTTPException(status_code=404, detail="Sport not found!")
    db_event = crud_event.create_event(db=db, event=event)
    return schemas.EventDTO(id=db_event.id, title=db_event.title, sport_name=db_sport.title)
