from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    JSONResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from datetime import datetime, date

from ..dependencies import get_db

from ..crud import event

from pathlib import Path

router = APIRouter(prefix="/event")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", response_class=HTMLResponse)
async def get_note(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("event/event.html", {"request": request})


@router.get("/list", response_class=HTMLResponse)
async def list_events(request: Request, db: Session = Depends(get_db)):
    events = event.get_all_events(db)
    return templates.TemplateResponse(
        "event/list.html", {"request": request, "events": events}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_event_form(request: Request, db: Session = Depends(get_db)):
    # pass today's date
    today = date.today().strftime("%Y-%m-%d")
    return templates.TemplateResponse("event/create.html", {"request": request, "today": today})


@router.post("/create")
async def create_quote(
    request: Request, db: Session = Depends(get_db), event_date: str = Form(...), event_text: str = Form(...), repeating: str = Form("")
):
    event_date = datetime.strptime(event_date, "%Y-%m-%d")
    if repeating == "true":
        event_repeat = True
    else:
        event_repeat = False
    event.add_new_event(db, event_date, event_text, event_repeat)

    return RedirectResponse("/event/list", status_code=303)


@router.post("/delete_event", response_class=HTMLResponse)
async def delete_event(
    request: Request, db: Session = Depends(get_db), action: str = Form(...)
):
    (action, event_id) = action.split("_")
    event_id = int(event_id)
    if action == "delete":
        deleted = event.delete_event_by_id(db, event_id)
        completed_action = "Deleted Event"

    return templates.TemplateResponse(
        "event/delete_event.html",
        {
            "request": request,
            "completed_action": completed_action,
            "event_id": event_id,
        },
    )


@router.get("/today", response_class=HTMLResponse)
async def events_today(request: Request, db: Session = Depends(get_db)):
    date_today = date.today()
    events = event.get_todays_events(db, date_today)
    return templates.TemplateResponse(
        "event/today.html", {"request": request, "events": events}
    )

@router.get("/today/json", response_class=JSONResponse)
async def get_settings(request: Request, db: Session = Depends(get_db)):
    # date_today = datetime.strftime(datetime.today(), "%Y-%m-%d")
    date_today = date.today()
    events = event.get_todays_events(db, date_today)
    return events


"""
date
message
it will appear on that day

no message to show for a given date:


"""
