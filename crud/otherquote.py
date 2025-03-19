from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models

from .state import *


def get_all_quotes(db: Session):
    return db.query(models.OtherQuote).all()


def choose_and_store_random_quote(db: Session):
    random_quote = db.query(models.OtherQuote).order_by(func.random()).first()
    while random_quote.id == get_current_other_quote_id(db):
        random_quote = db.query(models.OtherQuote).order_by(func.random()).first()
    update_state_other_quote_id(db, random_quote.id)
    update_state_quote_date(db)
    return random_quote


def return_today_quote(db: Session):
    quote_id = get_current_other_quote_id(db)
    quote = db.query(models.OtherQuote).filter(models.OtherQuote.id == quote_id).first()
    return quote


def choose_random_quote(db: Session):
    quoted_today = check_if_quote_today(db)
    if not quoted_today:
        quote = choose_and_store_random_quote(db)
    else:
        quote = return_today_quote(db)
    return quote


def get_random_quote_text(db: Session):
    quote = choose_random_quote(db)
    return f"{quote.quote} - {quote.author}"


def get_random_quote_json(db: Session):
    quote = choose_random_quote(db)
    return quote


def add_new_quote(db: Session, quote_text, quote_author):
    new_quote = models.OtherQuote()
    new_quote.quote = quote_text
    new_quote.author = quote_author
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return True

def delete_quote_by_id(db: Session, quote_id: int):
    to_delete = db.query(models.OtherQuote).filter(models.OtherQuote.id == quote_id).delete()
    if to_delete:
        db.commit()
        return True
    return False
