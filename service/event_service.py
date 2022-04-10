import random

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


def shuffle_players(event_id: int, db: Session):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found!")

    players_number = len(db_event.players)
    participants_number = db_event.sport.participants_number
    if players_number != participants_number:
        raise HTTPException(status_code=400, detail="Shuffle not possible!")

    players = db_event.players
    random.shuffle(players)
    for idx, player in enumerate(players):
        if idx < players_number / 2:
            team_nr = 1
        else:
            team_nr = 2
        crud_event.add_team_nr_to_player(db=db, player_id=player.id, team_nr=team_nr)

    crud_event.add_teams_created_true(db=db, event_id=db_event.id)
    return db_event


def swap_players(event_id: int, player_swap: schemas.PlayerSwap, db: Session):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found!")

    player_one = crud_event.get_player_by_id(db=db, player_id=player_swap.player_one_id)
    player_two = crud_event.get_player_by_id(db=db, player_id=player_swap.player_two_id)

    if not player_one or not player_two:
        raise HTTPException(status_code=404, detail="One of the players not found!")

    if player_one.team_nr == player_two.team_nr:
        raise HTTPException(status_code=400, detail="Players are in the same team!")

    temp_team_nr = player_one.team_nr
    crud_event.add_team_nr_to_player(db=db, player_id=player_swap.player_one_id, team_nr=player_two.team_nr)
    crud_event.add_team_nr_to_player(db=db, player_id=player_swap.player_two_id, team_nr=temp_team_nr)

    return db_event


def remove_player(event_id: int, player_id: int, db: Session):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found!")

    if db_event.teams_created:
        raise HTTPException(status_code=400, detail="Remove not possible!")

    crud_event.remove_player_by_id(db=db, player_id=player_id)
    return db_event


def edit_player(event_id: int, player_id: int, edited_player: schemas.NewPlayer, db: Session):
    db_event = crud_event.get_event_by_id(db=db, event_id=event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found!")

    crud_event.edit_player(db=db, player_id=player_id, edited_player=edited_player)
    return db_event
