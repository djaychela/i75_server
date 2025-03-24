from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from pydantic import BaseModel

from .. import models

from datetime import datetime

from .state import *

def get_all_events(db: Session):
    return db.query(models.Event).all()

def get_todays_events(db: Session, date_today):
    """Returns any event where the day and month match the datetime passed in, if repeating
    or exact match if not repeating"""
    todays_events = []
    all_events = db.query(models.Event).all()
    this_month = date_today.month
    this_day = date_today.day
    for event in all_events:
        if event.date.month == this_month and event.date.day == this_day and event.repeating:
            todays_events.append(event)
        elif event.date == date_today:
            todays_events.append(event)
    return todays_events

def add_new_event(db: Session, event_date, event_text, event_repeat):
    new_event = models.Event()
    new_event.date = event_date
    new_event.text = event_text
    new_event.repeating = event_repeat
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def delete_event_by_id(db: Session, event_id: int):
    to_delete = db.query(models.Event).filter(models.Event.id == event_id).delete()
    if to_delete:
        db.commit()
        return True
    return False