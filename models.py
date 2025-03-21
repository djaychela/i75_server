from sqlalchemy import Column, Integer, String, JSON, Boolean, Date
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class DarrenQuote(Base):
    __tablename__ = "darrenquote_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quote = Column(String, index=True)

class DarrenNames(Base):
    __tablename__ = "darrennames_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name = Column(String, index=True)

class OtherQuote(Base):
    __tablename__ = "otherquote_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quote = Column(String, index=True)
    author = Column(String, index=True)

class Reminder(Base):
    __tablename__ = "reminder_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text = Column(String, index=True)
    date = Column(String, index=True)
    time = Column(String, index=True)

class ImageData(Base):
    __tablename__ = "imagedata_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text = Column(String, index=True)
    filename = Column(String)

class State(Base):
    __tablename__ = "state_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quote_date = Column(Date)
    other_quote_date = Column(Date)
    current_dj_quote_id = Column(Integer)
    current_dj_author_id = Column(Integer)
    current_other_quote_id = Column(Integer)

