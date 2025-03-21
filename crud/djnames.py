from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from pydantic import BaseModel

from .. import models

from .state import *


def get_all_names(db: Session):
    return db.query(models.DarrenNames).all()


def add_new_name(db: Session, quote_text):
    new_name = models.DarrenNames()
    new_name.name = quote_text
    db.add(new_name)
    db.commit()
    db.refresh(new_name)
    return True


def delete_name_by_id(db: Session, quote_id: int):
    to_delete = (
        db.query(models.DarrenNames).filter(models.DarrenNames.id == quote_id).delete()
    )
    if to_delete:
        db.commit()
        return True
    return False
