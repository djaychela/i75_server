from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from ..dependencies import get_db

from ..crud import state

from ..api import car_api

from ..helpers import car_helpers

from pathlib import Path

router = APIRouter(prefix="/car")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/api_values")
async def get_settings(request: Request, db: Session = Depends(get_db)):
    car_api_values = state.get_car_api_values(db)
    print(f"{car_api_values=}")
    api_base_values = car_helpers.build_api_namedtuple(car_api_values)
    print(f"{api_base_values=}")
    return templates.TemplateResponse(
        "car/api_values.html", {"request": request, "api_values": api_base_values}
    )


@router.post("/api_values", response_class=HTMLResponse)
async def store_settings(
    request: Request,
    db: Session = Depends(get_db),
    ha_base_url_value: str = Form(""),
    battery_api_url_value: str = Form(""),
    zappi_url_value: str = Form(""),
    charging_api_url_value: str = Form(""),
    zappi_rate_url_value: str = Form(""),
):
    car_api_values_dict = {
        "ha_base_url": ha_base_url_value,
        "battery_api_url": battery_api_url_value,
        "zappi_url": zappi_url_value,
        "charging_api_url": charging_api_url_value,
        "zappi_rate_url": zappi_rate_url_value,
    }
    car_api_values = state.store_car_api_values(db, car_api_values_dict)
    print(f"{car_api_values_dict=}")
    api_base_values = car_helpers.build_api_namedtuple(car_api_values)
    return templates.TemplateResponse(
        "car/api_values.html", {"request": request, "api_values": api_base_values}
    )


@router.get("/json", response_class=JSONResponse)
async def get_car_values_json(request: Request, db: Session = Depends(get_db)):
    car_data = car_api.get_car_api_data(db)
    return car_data
