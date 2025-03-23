from fastapi import FastAPI, applications
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

from . import models
from .database import engine
from .routers import home, djquote, otherquote, images, time, darren_names, settings, note, bin_day

from pathlib import Path
from os import path
import pathlib

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_PATH = Path(__file__).resolve().parent
upload_path = BASE_PATH / "uploads"

assets_path = str(pathlib.Path(__file__).parent.resolve() / "static")
if path.exists(assets_path + "/swagger-ui.css") and path.exists(
    assets_path + "/swagger-ui-bundle.js"
):
    app.mount("/assets", StaticFiles(directory=assets_path), name="static")
    app.mount("/uploads", StaticFiles(directory=upload_path))

    def swagger_monkey_patch(*args, **kwargs):
        return get_swagger_ui_html(
            *args,
            **kwargs,
            swagger_favicon_url="",
            swagger_css_url="/assets/swagger-ui.css",
            swagger_js_url="/assets/swagger-ui-bundle.js",
        )

    applications.get_swagger_ui_html = swagger_monkey_patch

app.include_router(home.router)
app.include_router(djquote.router)
app.include_router(otherquote.router)
app.include_router(images.router)
app.include_router(time.router)
app.include_router(darren_names.router)
app.include_router(settings.router)
app.include_router(note.router)
app.include_router(bin_day.router)
