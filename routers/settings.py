from fastapi import APIRouter, Depends, Request, Form, HTTPException, status, FastAPI, File, UploadFile
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import (
    JSONResponse,
    HTMLResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import secrets
import aiofiles

from typing import Annotated

from datetime import datetime
from pathlib import Path

from ..crud import state
from ..dependencies import get_db

security = HTTPBasic()

ALL_MODES = [
    "digital_clock_12",
    "quote_viewer",
    "cubes",
    "jpg_viewer",
    "balls",
    "rainbow",
    "digital_clock_24",
    "famous_quote_viewer",
    "warp_speed",
    "jpg_viewer_2",
    "spiral",
    "car",
    "note",
    "bin_day",
    "event",
    "wifi",
    "weather",
]


BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

router = APIRouter(prefix="/settings")

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"tammie"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"gggg"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@router.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("settings/settings.html", {"request": request})


@router.get("/json", response_class=JSONResponse)
async def get_settings(request: Request, db: Session = Depends(get_db)):
    date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    display_time = 10
    active_modes = state.get_active_modes(db)
    mode_times = state.get_mode_times(db)
    settings_dict = {
        "datetime": date_time,
        "display_time": display_time,
        "active_modes": active_modes,
        "mode_times": mode_times,
    }
    return settings_dict


@router.get("/modules", response_class=HTMLResponse)
# async def settings(username: Annotated[str, Depends(get_current_username)], request: Request, db: Session = Depends(get_db)):
async def modules(request: Request, db: Session = Depends(get_db)):
    current_state = state.get_state(db)
    current_active_modes = state.get_active_modes(db)
    active_modes = {}
    for mode in ALL_MODES:
        if mode in current_active_modes:
            active_modes[mode] = True
        else:
            active_modes[mode] = False
    mode_times = state.get_mode_times(db)
    return templates.TemplateResponse(
        "settings/modules.html",
        {
            "request": request,
            "active_modes": active_modes,
            "mode_times": mode_times,
        },
    )


@router.post("/modules", response_class=HTMLResponse)
async def store_settings(
    request: Request,
    db: Session = Depends(get_db),
    digital_clock_12: str = Form(""),
    quote_viewer: str = Form(""),
    cubes: str = Form(""),
    jpg_viewer: str = Form(""),
    balls: str = Form(""),
    rainbow: str = Form(""),
    digital_clock_24: str = Form(""),
    famous_quote_viewer: str = Form(""),
    warp_speed: str = Form(""),
    jpg_viewer_2: str = Form(""),
    spiral: str = Form(""),
    car: str = Form(""),
    note: str = Form(""),
    bin_day: str = Form(""),
    event: str = Form(""),
    wifi: str = Form(""),
    weather: str = Form(""),
    digital_clock_12_time: int = Form(""),
    quote_viewer_time: int = Form(""),
    cubes_time: int = Form(""),
    jpg_viewer_time: int = Form(""),
    balls_time: int = Form(""),
    rainbow_time: int = Form(""),
    digital_clock_24_time: int = Form(""),
    famous_quote_viewer_time: int = Form(""),
    warp_speed_time: int = Form(""),
    jpg_viewer_2_time: int = Form(""),
    spiral_time: int = Form(""),
    car_time: int = Form(""),
    note_time: int = Form(""),
    bin_day_time: int = Form(""),
    event_time: int = Form(""),
    wifi_time: int = Form(""),
    weather_time: int = Form(""),
):

    modes_to_check = {
        "digital_clock_12": digital_clock_12,
        "quote_viewer": quote_viewer,
        "cubes": cubes,
        "jpg_viewer": jpg_viewer,
        "balls": balls,
        "rainbow": rainbow,
        "digital_clock_24": digital_clock_24,
        "famous_quote_viewer": famous_quote_viewer,
        "warp_speed": warp_speed,
        "jpg_viewer_2": jpg_viewer_2,
        "spiral": spiral,
        "car": car,
        "note": note,
        "bin_day": bin_day,
        "event": event,
        "wifi": wifi,
        "weather": weather,
    }

    times_to_check = {
        "digital_clock_12": digital_clock_12_time,
        "quote_viewer": quote_viewer_time,
        "cubes": cubes_time,
        "jpg_viewer": jpg_viewer_time,
        "balls": balls_time,
        "rainbow": rainbow_time,
        "digital_clock_24": digital_clock_24_time,
        "famous_quote_viewer": famous_quote_viewer_time,
        "warp_speed": warp_speed_time,
        "jpg_viewer_2": jpg_viewer_2_time,
        "spiral": spiral_time,
        "car": car_time,
        "note": note_time,
        "bin_day": bin_day_time,
        "event": event_time,
        "wifi" : wifi_time,
        "weather": weather_time,
    }

    modes_from_form = [key for key, value in modes_to_check.items() if value == "true"]
    updated_modes = state.store_active_modes(db, modes_from_form)

    times_from_form = {key: value for key, value in times_to_check.items()}
    updated_mode_times = state.store_mode_times(db, times_from_form)

    active_modes = {}
    for mode in ALL_MODES:
        if mode in updated_modes:
            active_modes[mode] = True
        else:
            active_modes[mode] = False

    return templates.TemplateResponse(
        "settings/modules.html",
        {
            "request": request,
            "active_modes": active_modes,
            "mode_times": updated_mode_times,
        },
    )


@router.get("/database")
async def database(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("settings/database.html", {"request": request})


@router.post("/uploadfile/", response_class=HTMLResponse)
async def create_upload_file(request: Request, file: UploadFile):
    # replace database file...
    file_path = Path(__file__).resolve().parent.parent / "storage" / "i75data.db"
    print(f"{file_path=}")
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()  # async read
        await out_file.write(content)  # async write

    return templates.TemplateResponse("settings/database.html", {"request": request})