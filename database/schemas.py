from pydantic import BaseModel


class SportBase(BaseModel):
    title: str


class Sport(SportBase):
    id: int

    class Config:
        orm_mode = True
