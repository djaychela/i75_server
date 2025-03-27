from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session


from ..dependencies import get_db

from ..crud import state

from ..api import ha_api


from pathlib import Path

router = APIRouter(prefix="/ha")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))


@router.get("/api_values")
async def get_settings(request: Request, db: Session = Depends(get_db)):
    ha_api_values = state.get_ha_api_values(db)
    print(ha_api_values)
    return templates.TemplateResponse(
        "ha/api_values.html", {"request": request, "api_values": ha_api_values}
    )


@router.post("/api_values", response_class=HTMLResponse)
async def store_settings(
    request: Request,
    db: Session = Depends(get_db),
    name_2: str = Form(""),
    name_3: str = Form(""),
    name_4: str = Form(""),
    name_5: str = Form(""),
    name_6: str = Form(""),
    name_7: str = Form(""),
    name_8: str = Form(""),
    name_9: str = Form(""),
    name_10: str = Form(""),
    value_1: str = Form(""),
    value_2: str = Form(""),
    value_3: str = Form(""),
    value_4: str = Form(""),
    value_5: str = Form(""),
    value_6: str = Form(""),
    value_7: str = Form(""),
    value_8: str = Form(""),
    value_9: str = Form(""),
    value_10: str = Form(""),
    units_2: str = Form(""),
    units_3: str = Form(""),
    units_4: str = Form(""),
    units_5: str = Form(""),
    units_6: str = Form(""),
    units_7: str = Form(""),
    units_8: str = Form(""),
    units_9: str = Form(""),
    units_10: str = Form(""),
    type_2: str = Form(""),
    type_3: str = Form(""),
    type_4: str = Form(""),
    type_5: str = Form(""),
    type_6: str = Form(""),
    type_7: str = Form(""),
    type_8: str = Form(""),
    type_9: str = Form(""),
    type_10: str = Form(""),
    min_2: int = Form(""),
    min_3: int = Form(""),
    min_4: int = Form(""),
    min_5: int = Form(""),
    min_6: int = Form(""),
    min_7: int = Form(""),
    min_8: int = Form(""),
    min_9: int = Form(""),
    min_10: int = Form(""),
    max_2: int = Form(""),
    max_3: int = Form(""),
    max_4: int = Form(""),
    max_5: int = Form(""),
    max_6: int = Form(""),
    max_7: int = Form(""),
    max_8: int = Form(""),
    max_9: int = Form(""),
    max_10: int = Form(""),
):  # Note: Fewer values for 1 as it is fixed to be the api base URL!
    # Note: disconnect in value key and stored values.
    ha_api_values_dict = {
        "api_url": ["Base URL of Home Assistant", value_1],
        "value_1": [name_2, value_2, units_2, type_2, min_2, max_2],
        "value_2": [name_3, value_3, units_3, type_3, min_3, max_3],
        "value_3": [name_4, value_4, units_4, type_4, min_4, max_4],
        "value_4": [name_5, value_5, units_5, type_5, min_5, max_5],
        "value_5": [name_6, value_6, units_6, type_6, min_6, max_6],
        "value_6": [name_7, value_7, units_7, type_7, min_7, max_7],
        "value_7": [name_8, value_8, units_8, type_8, min_8, max_8],
        "value_8": [name_9, value_9, units_9, type_9, min_9, max_9],
        "value_9": [name_10, value_10, units_10, type_10, min_10, max_10],
    }
    print(ha_api_values_dict)
    ha_api_values = state.store_ha_api_values(db, ha_api_values_dict)
    return templates.TemplateResponse(
        "ha/api_values.html", {"request": request, "api_values": ha_api_values}
    )


@router.get("/json", response_class=JSONResponse)
async def get_ha_values_json(request: Request, db: Session = Depends(get_db)):
    car_data = ha_api.get_ha_api_data(db)
    return car_data
