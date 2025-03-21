from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from datetime import datetime, date

from pydantic import BaseModel

from .. import models


def get_state(db: Session):
    return db.query(models.State).filter(models.State.id == 1).first()


def check_if_dj_quote_today(db: Session):
    current_state = get_state(db)
    return current_state.quote_date == date.today()

def check_if_other_quote_today(db: Session):
    current_state = get_state(db)
    return current_state.other_quote_date == date.today()


def update_state_dj_quote_date(db: Session):
    current_state = get_state(db)
    current_state.quote_date = datetime.today()
    db.commit()

def update_state_other_quote_date(db: Session):
    current_state = get_state(db)
    current_state.other_quote_date = datetime.today()
    db.commit()


def update_state_dj_quote_id(db: Session, id: int):
    current_state = get_state(db)
    current_state.current_dj_quote_id = id
    db.commit()


def update_state_other_quote_id(db: Session, id: int):
    current_state = get_state(db)
    current_state.current_other_quote_id = id
    db.commit()


def update_state_dj_author_id(db: Session, id: int):
    current_state = get_state(db)
    current_state.current_dj_author_id = id
    db.commit()


def get_current_dj_quote_id(db):
    current_state = get_state(db)
    return current_state.current_dj_quote_id


def get_current_dj_author_id(db):
    current_state = get_state(db)
    return current_state.current_dj_author_id


def get_current_other_quote_id(db):
    current_state = get_state(db)
    return current_state.current_other_quote_id