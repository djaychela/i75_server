from sqlalchemy import Column, Integer, String, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class DarrenQuote(Base):
    __tablename__ = "darrenquote_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quote = Column(String, index=True)

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

