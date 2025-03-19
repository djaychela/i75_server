from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from datetime import date

from ..dependencies import get_db

from ..crud import djquote, state

from pathlib import Path

router = APIRouter(prefix="/djquote")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("djquote/djquote.html", {"request": request})


@router.get("/list", response_class=HTMLResponse)
async def list_quotes(request: Request, db: Session = Depends(get_db)):
    quotes = djquote.get_all_quotes(db)
    return templates.TemplateResponse(
        "djquote/list.html", {"request": request, "quotes": quotes}
    )


@router.get("/random", response_class=PlainTextResponse)
async def random(request: Request, db: Session = Depends(get_db)):
    quote, author = djquote.choose_random_quote(db)
    return quote.quote

@router.get("/randomjson", response_class=JSONResponse)
async def random(request: Request, db: Session = Depends(get_db)):
    quote = djquote.get_random_quote_json(db)
    return quote

@router.get("/randomhtml", response_class=HTMLResponse)
async def random(request: Request, db: Session = Depends(get_db)):
    quote, author = djquote.choose_random_quote(db)
    return templates.TemplateResponse(
        "djquote/random.html", {"request": request, "quote": quote, "author": author}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_quote_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("djquote/create.html", {"request": request})


@router.post("/create")
async def create_quote(
    request: Request, db: Session = Depends(get_db), content: str = Form(...)
):
    djquote.add_new_quote(db, content)
    return RedirectResponse("/djquote/list", status_code=303)

@router.post("/delete_quote", response_class=HTMLResponse)
async def delete_image(
    request: Request, db: Session = Depends(get_db), action: str = Form(...)
):
    (action, quote_id) = action.split("_")
    quote_id = int(quote_id)
    if action == "delete":
        deleted = djquote.delete_quote_by_id(db, quote_id=quote_id)
        completed_action = "Deleted Quote"

    return templates.TemplateResponse(
        "djquote/delete_quote.html",
        {
            "request": request,
            "completed_action": completed_action,
            "quote_id": quote_id,
        },
    )