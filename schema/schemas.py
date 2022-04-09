from pydantic import BaseModel


class SportBase(BaseModel):
    title: str


class Sport(SportBase):
    id: int

    class Config:
        orm_mode = True


class EventBase(BaseModel):
    title: str
    sport_id: int


class Event(EventBase):
    id: int

    class Config:
        orm_mode = True


class EventDTO(BaseModel):
    id: int
    title: str
    sport_name: str
