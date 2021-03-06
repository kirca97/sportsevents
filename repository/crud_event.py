from fastapi import HTTPException
from sqlalchemy.orm import Session

from model import models
from schema import schemas


def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Event).offset(skip).limit(limit).all()


def get_event_by_id(db: Session, event_id: int):
    return db.query(models.Event).filter(models.Event.id == event_id).first()


def create_event(db: Session, event: schemas.EventBase):
    db_event = models.Event(title=event.title, sport_id=event.sport_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def edit_event_name(db: Session, event_id: int, event_title: str):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db_event.title = event_title
    db.add(db_event)
    db.commit()
    db.refresh(db_event)


def add_player(db: Session, event_id: int, player: schemas.NewPlayer):
    db_player = models.Player(name=player.name, email=player.email, event_id=event_id)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)


def add_team_nr_to_player(db: Session, player_id: int, team_nr: int):
    db_player = db.query(models.Player).filter(models.Player.id == player_id).first()
    db_player.team_nr = team_nr
    db.add(db_player)
    db.commit()
    db.refresh(db_player)


def add_teams_created_true(db: Session, event_id: int):
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    db_event.teams_created = True
    db.add(db_event)
    db.commit()
    db.refresh(db_event)


def get_player_by_id(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def remove_player_by_id(db: Session, player_id: int):
    player = get_player_by_id(db=db, player_id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found!")

    db.delete(player)
    db.commit()


def edit_player(db: Session, player_id: int, edited_player: schemas.NewPlayer):
    player = get_player_by_id(db=db, player_id=player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found!")

    player.name = edited_player.name
    player.email = edited_player.email
    db.add(player)
    db.commit()
    db.refresh(player)
