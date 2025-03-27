from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from datetime import datetime, date

from pydantic import BaseModel

import json

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


def get_active_modes(db):
    current_state = get_state(db)
    return json.loads(current_state.active_modes)


def get_mode_times(db):
    current_state = get_state(db)
    return json.loads(current_state.mode_times)


def store_active_modes(db: Session, active_modes: list):
    current_state = get_state(db)
    active_modes_json = json.dumps(active_modes)
    current_state.active_modes = active_modes_json
    db.commit()
    return json.loads(current_state.active_modes)


def store_mode_times(db: Session, mode_times: dict):
    current_state = get_state(db)
    mode_times_json = json.dumps(mode_times)
    current_state.mode_times = mode_times_json
    db.commit()
    return json.loads(current_state.mode_times)

def check_if_bin_date_today(db: Session):
    current_state = get_state(db)
    return current_state.bin_date == date.today()

def set_bin_date_to_today(db: Session):
    current_state = get_state(db)
    current_state.bin_date = date.today()
    db.commit()
    return current_state.bin_date

def store_bin_info(db: Session, bin_info: list):
    current_state = get_state(db)
    current_state.bin_info = json.dumps(bin_info)
    db.commit()
    return json.loads(current_state.bin_info)

def get_bin_info(db: Session):
    current_state = get_state(db)
    return json.loads(current_state.bin_info)

def get_display_times(db: Session):
    current_state = get_state(db)
    return (current_state.display_start, current_state.display_end)

def set_display_times(db: Session, display_start, display_end):
    current_state = get_state(db)
    current_state.display_start = display_start
    current_state.display_end = display_end
    db.commit()
    return (current_state.display_start, current_state.display_end)

def get_mode_colours(db):
    current_state = get_state(db)
    return json.loads(current_state.mode_colours)

def store_mode_colours(db: Session, mode_colours: dict):
    current_state = get_state(db)
    mode_colours_json = json.dumps(mode_colours)
    current_state.mode_colours = mode_colours_json
    db.commit()
    return json.loads(current_state.mode_colours)

def get_car_api_values(db):
    current_state = get_state(db)
    return json.loads(current_state.car_api_values)

def store_car_api_values(db: Session, car_api_values: dict):
    current_state = get_state(db)
    car_api_values_json = json.dumps(car_api_values)
    current_state.car_api_values = car_api_values_json
    db.commit()
    return json.loads(current_state.car_api_values)

def get_ha_api_values(db):
    current_state = get_state(db)
    return json.loads(current_state.ha_api_values)

def store_ha_api_values(db: Session, ha_api_values: dict):
    current_state = get_state(db)
    ha_api_valuess_json = json.dumps(ha_api_values)
    current_state.ha_api_values = ha_api_valuess_json
    db.commit()
    return json.loads(current_state.ha_api_values)