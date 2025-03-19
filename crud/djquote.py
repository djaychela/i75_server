from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from pydantic import BaseModel

from .. import models

from .state import *


def get_all_quotes(db: Session):
    return db.query(models.DarrenQuote).all()


def choose_and_store_random_quote(db: Session):
    random_quote = db.query(models.DarrenQuote).order_by(func.random()).first()
    random_author = db.query(models.DarrenNames).order_by(func.random()).first()
    update_state_dj_quote_id(db, random_quote.id)
    update_state_dj_author_id(db, random_author.id)
    update_state_quote_date(db)
    return (random_quote, random_author)


def return_today_quote(db: Session):
    quote_id = get_current_dj_quote_id(db)
    author_id = get_current_dj_author_id(db)
    quote = (
        db.query(models.DarrenQuote).filter(models.DarrenQuote.id == quote_id).first()
    )
    author = (
        db.query(models.DarrenNames).filter(models.DarrenNames.id == author_id).first()
    )
    return (quote, author)


def choose_random_quote(db: Session):
    quoted_today = check_if_quote_today(db)
    if not quoted_today:
        quote = choose_and_store_random_quote(db)
    else:
        quote = return_today_quote(db)
    return quote


def get_random_quote_json(db: Session):
    class DarrenJsonQuote(BaseModel):
        quote: str
        author: str

    quoted_today = check_if_quote_today(db)
    if not quoted_today:
        quote, name = choose_and_store_random_quote(db)
    else:
        quote, name = return_today_quote(db)
    json_data = DarrenJsonQuote(quote=quote.quote, author=name.name)
    return json_data


def get_random_quote_author(db: Session):
    author = db.query(models.DarrenNames).order_by(func.random()).first()
    return author.name


def get_current_quote_author(db: Session):
    dj_quote_id = get_current_dj_quote_id
    author = db.query(models.DarrenNames).order_by(func.random()).first()
    return author.name


def get_random_quote_text(db: Session):
    quoted_today = check_if_quote_today(db)
    if not quoted_today:
        choose_and_store_random_quote(db)


def get_random_quote_text(db: Session):
    quoted_today = check_if_quote_today(db)
    if not quoted_today:
        choose_and_store_random_quote(db)
    quote = db.query(models.DarrenQuote).order_by(func.random()).first()
    return quote.quote


def add_new_quote(db: Session, quote_text):
    new_quote = models.DarrenQuote()
    new_quote.quote = quote_text
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return True
