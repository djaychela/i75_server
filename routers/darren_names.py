from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    JSONResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from datetime import date

from ..dependencies import get_db

from ..crud import djnames, djquote, state

from pathlib import Path

router = APIRouter(prefix="/djnames")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("djnames/djnames.html", {"request": request})


@router.get("/list", response_class=HTMLResponse)
async def list_quotes(request: Request, db: Session = Depends(get_db)):
    names = djnames.get_all_names(db)
    return templates.TemplateResponse(
        "djnames/list.html", {"request": request, "names": names}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_quote_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("djnames/create.html", {"request": request})


@router.post("/create")
async def create_quote(
    request: Request, db: Session = Depends(get_db), content: str = Form(...)
):
    djnames.add_new_name(db, content)
    return RedirectResponse("/djnames/list", status_code=303)


@router.post("/delete_name", response_class=HTMLResponse)
async def delete_image(
    request: Request, db: Session = Depends(get_db), action: str = Form(...)
):
    (action, quote_id) = action.split("_")
    quote_id = int(quote_id)
    if action == "delete":
        deleted = djnames.delete_name_by_id(db, quote_id=quote_id)
        completed_action = "Deleted Name"

    return templates.TemplateResponse(
        "djnames/delete_name.html",
        {
            "request": request,
            "completed_action": completed_action,
            "quote_id": quote_id,
        },
    )
