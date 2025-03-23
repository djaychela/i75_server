from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from .. import models

# from .state import *

def get_note(db: Session):
    return db.query(models.Note).filter(models.Note.id == 1).first()


def edit_note(db: Session, note_text):
    note_to_edit = db.query(models.Note).filter(models.Note.id == 1).first()
    note_to_edit.text = note_text
    db.add(note_to_edit)
    db.commit()
    db.refresh(note_to_edit)
    return note_to_edit



