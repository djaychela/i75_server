from fastapi import APIRouter, Depends, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..schemas.image import ImageFile

from pathlib import Path

router = APIRouter(prefix="/images")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
upload_path = BASE_PATH.parent / "uploads" / "images"

@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("images/index.html", {"request": request})

@router.post("/submit")
async def submit(image: UploadFile, image_file: ImageFile = Depends(ImageFile)):
    file_path = upload_path / image.filename
    with open(file_path, "wb") as f:
        f.write(await image.read())
    return {
        "name": image_file.name,
        "image": image.filename
    }