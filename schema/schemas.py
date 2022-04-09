from pydantic import BaseModel


class SportBase(BaseModel):
    title: str
    participants_number: int


class Sport(SportBase):
    id: int

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    name: str
    email: str | None
    event_id: int


class Player(PlayerBase):
    id: int
    team_nr: int | None

    class Config:
        orm_mode = True


class NewPlayer(BaseModel):
    name: str
    email: str = None


class EventBase(BaseModel):
    title: str
    sport_id: int


class Event(EventBase):
    id: int
    teams_created: bool
    players: list[Player] = []

    class Config:
        orm_mode = True


class EditEvent(BaseModel):
    title: str = None
    players: list[NewPlayer]
