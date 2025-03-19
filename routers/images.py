from fastapi import APIRouter, Depends, Request, Form, UploadFile
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    FileResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..schemas.image import ImageFile

from ..crud import images
from ..helpers import image_helpers


from pathlib import Path

router = APIRouter(prefix="/images")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
upload_path = BASE_PATH.parent / "uploads" / "images"


@router.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("images/images.html", {"request": request})


@router.get("/upload")
async def upload(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("images/upload.html", {"request": request})


@router.post("/submit")
async def submit(
    image: UploadFile,
    request: Request,
    image_text: ImageFile = Depends(ImageFile),
    db: Session = Depends(get_db),
):
    # file_path = upload_path / image.filename
    new_filename = image_helpers.add_prefix(image.filename)
    print(f"{new_filename=}")
    file_path = upload_path / new_filename
    with open(file_path, "wb") as f:
        f.write(await image.read())
    images.store_new_image(db, image_text.name, new_filename)
    return {"name": image_text.name, "image": new_filename}


@router.get("/random")
async def index(request: Request, db: Session = Depends(get_db)):
    filename = images.get_random_image_filename(db)
    file_path = upload_path / filename
    return FileResponse(file_path)


@router.get("/list", response_class=HTMLResponse)
async def list_quotes(request: Request, db: Session = Depends(get_db)):
    image_list = images.get_all_images(db)
    return templates.TemplateResponse(
        "images/list.html", {"request": request, "images": image_list}
    )


@router.post("/delete_image", response_class=HTMLResponse)
async def delete_image(
    request: Request, db: Session = Depends(get_db), action: str = Form(...)
):
    (action, image_id) = action.split("_")
    image_id = int(image_id)
    if action == "delete":
        file_to_delete = images.get_image_filename(db, image_id=image_id)
        file_path = upload_path / file_to_delete
        file_path.unlink()
        deleted = images.delete_image_by_id(db, image_id=image_id)
        completed_action = "Deleted Image"

    return templates.TemplateResponse(
        "images/delete_image.html",
        {
            "request": request,
            "completed_action": completed_action,
            "image_id": image_id,
        },
    )
