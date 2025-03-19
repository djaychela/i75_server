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

from ..crud import otherquote

from pathlib import Path

router = APIRouter(prefix="/otherquote")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(
        "otherquote/otherquote.html", {"request": request}
    )


@router.get("/list", response_class=HTMLResponse)
async def list_quotes(request: Request, db: Session = Depends(get_db)):
    quotes = otherquote.get_all_quotes(db)
    return templates.TemplateResponse(
        "otherquote/list.html", {"request": request, "quotes": quotes}
    )


@router.get("/random", response_class=PlainTextResponse)
async def random(request: Request, db: Session = Depends(get_db)):
    quote = otherquote.get_random_quote_text(db)
    return quote


@router.get("/randomjson", response_class=JSONResponse)
async def random(request: Request, db: Session = Depends(get_db)):
    quote = otherquote.get_random_quote_json(db)
    return quote


@router.get("/randomhtml", response_class=HTMLResponse)
async def random(request: Request, db: Session = Depends(get_db)):
    quote = otherquote.choose_random_quote(db)
    return templates.TemplateResponse(
        "otherquote/random.html", {"request": request, "quote": quote}
    )


@router.get("/create", response_class=HTMLResponse)
async def create_quote_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("otherquote/create.html", {"request": request})


@router.post("/create")
async def create_quote(
    request: Request,
    db: Session = Depends(get_db),
    quote: str = Form(...),
    author: str = Form(...),
):
    otherquote.add_new_quote(db, quote, author)
    return RedirectResponse("/otherquote/list", status_code=303)


@router.post("/delete_quote", response_class=HTMLResponse)
async def delete_image(
    request: Request, db: Session = Depends(get_db), action: str = Form(...)
):
    (action, quote_id) = action.split("_")
    quote_id = int(quote_id)
    if action == "delete":
        deleted = otherquote.delete_quote_by_id(db, quote_id=quote_id)
        completed_action = "Deleted Quote"

    return templates.TemplateResponse(
        "otherquote/delete_quote.html",
        {
            "request": request,
            "completed_action": completed_action,
            "quote_id": quote_id,
        },
    )
