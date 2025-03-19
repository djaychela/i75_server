from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, JSONResponse
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
    return templates.TemplateResponse("otherquote/otherquote.html", {"request": request})


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

@router.get("/create", response_class=HTMLResponse)
async def create_quote_form(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("otherquote/create.html", {"request": request})


@router.post("/create")
async def create_quote(
    request: Request, db: Session = Depends(get_db), quote: str = Form(...), author: str = Form(...)
):
    otherquote.add_new_quote(db, quote, author)
    return RedirectResponse("/otherquote/list", status_code=303)

# @router.get("/import", response_class=PlainTextResponse)
# async def random(request: Request, db: Session = Depends(get_db)):
#     quote = otherquote.import_from_text(db)
#     return quote