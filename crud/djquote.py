from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models


def get_all_quotes(db: Session):
    return db.query(models.DarrenQuote).all()


def get_random_quote_text(db: Session):
    quote = db.query(models.DarrenQuote).order_by(func.random()).first()
    return quote.quote


def add_new_quote(db: Session, quote_text):
    new_quote = models.DarrenQuote()
    new_quote.quote = quote_text
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return True
