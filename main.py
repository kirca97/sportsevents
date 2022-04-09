from typing import List

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from config.database import SessionLocal, engine
from model import models
from schema import schemas
from service import sport_service, event_service

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/sports", response_model=List[schemas.Sport])
def get_sports(db: Session = Depends(get_db)):
    return sport_service.get_sports(db=db)


@app.post("/sports", response_model=schemas.Sport)
def create_sport(sport: schemas.SportBase, db: Session = Depends(get_db)):
    return sport_service.create_sport(db=db, sport=sport)


@app.get("/events", response_model=List[schemas.Event])
def get_events(db: Session = Depends(get_db)):
    return event_service.get_events(db=db)


@app.post("/events", response_model=schemas.Event)
def create_event(event: schemas.EventBase, db: Session = Depends(get_db)):
    return event_service.create_event(db=db, event=event)


@app.patch("/events/{event_id}", response_model=schemas.Event)
def edit_event(event_id: int, edited_event: schemas.EditEvent, db: Session = Depends(get_db)):
    return event_service.edit_event(event_id=event_id, edited_event=edited_event, db=db)
