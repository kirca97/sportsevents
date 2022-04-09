from fastapi import HTTPException
from sqlalchemy.orm import Session

from repository import crud_event, crud_sport
from schema import schemas


def get_events(db: Session):
    events = crud_event.get_events(db=db)
    return events


def create_event(db: Session, event: schemas.EventBase):
    db_sport = crud_sport.get_sport_by_id(db=db, id=event.sport_id)
    if not db_sport:
        raise HTTPException(status_code=404, detail="Sport not found!")

    db_event = crud_event.create_event(db=db, event=event)
    return db_event


def edit_event(event_id: int, edited_event: schemas.EditEvent, db: Session):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found!")

    if edited_event.title:
        crud_event.edit_event_name(db=db, event_id=event_id, event_title=edited_event.title)

    for new_player in edited_event.players:
        crud_event.add_player(db=db, event_id=event_id, player=new_player)

    return db_event
