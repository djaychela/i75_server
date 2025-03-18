from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models


def get_all_quotes(db: Session):
    return db.query(models.OtherQuote).all()


def get_random_quote_text(db: Session):
    quote = db.query(models.OtherQuote).order_by(func.random()).first()
    return f"{quote.quote} - {quote.author}"


def add_new_quote(db: Session, quote_text, quote_author):
    new_quote = models.OtherQuote()
    new_quote.quote = quote_text
    new_quote.author = quote_author
    db.add(new_quote)
    db.commit()
    db.refresh(new_quote)
    return True

# def import_from_text(db: Session):
#     from pathlib import Path
#     file_path = str(Path(__file__).parent.resolve())
#     print(f"{file_path=}")
                    
#     with open(f"{file_path}/other_quotes.txt", "r") as file:
#         for line in file.readlines():
#             print(f"{line.strip().split("-")=}")
#             quote_text, quote_author = line.strip().split("-")
#             new_quote = models.OtherQuote()
#             new_quote.quote = quote_text
#             new_quote.author = quote_author
#             db.add(new_quote)
#             db.commit()
#             db.refresh(new_quote)