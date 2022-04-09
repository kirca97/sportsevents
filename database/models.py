from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Sport(Base):
    __tablename__ = "sport"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)

    events = relationship("Event", back_populates="sport")


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    sport_id = Column(Integer, ForeignKey("sport.id"))

    sport = relationship("Sport", back_populates="events")


class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    team_nr = Column(Integer)
    event_id = Column(Integer, ForeignKey("event.id"))

    event = relationship("Event")
