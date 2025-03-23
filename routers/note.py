from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    JSONResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..crud import note

from pathlib import Path

router = APIRouter(prefix="/note")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", response_class=HTMLResponse)
async def get_note(request: Request, db: Session = Depends(get_db)):
    current_note = note.get_note(db)
    return templates.TemplateResponse(
        "note/note.html", {"request": request, "current_note": current_note}
    )


@router.post("/")
async def edit_note(
    request: Request,
    db: Session = Depends(get_db),
    note_text: str = Form(...),
):
    note.edit_note(db, note_text)
    return RedirectResponse("/note/", status_code=303)


@router.get("/json", response_class=JSONResponse)
async def get_settings(request: Request, db: Session = Depends(get_db)):
    current_note = note.get_note(db)
    # note_dict = {
    #     "datetime": date_time,
    #     "display_time": display_time,
    #     "active_modes": active_modes,
    #     "mode_times": mode_times,
    # }
    return current_note
