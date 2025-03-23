from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import (
    HTMLResponse,
    PlainTextResponse,
    RedirectResponse,
    JSONResponse,
)
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from datetime import datetime, date
from datetime import timedelta
import requests

from ..dependencies import get_db

from ..crud import state

from pathlib import Path

router = APIRouter(prefix="/bin_day")

BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

BIN_URL = (
    "https://online.bcpcouncil.gov.uk/bcp-apis/?api=BinDayLookup&uprn=100040763050"
)


def suffix(d):
    return {1: "st", 2: "nd", 3: "rd"}.get(d % 20, "th")


def custom_strftime(format, t):
    return t.strftime(format).replace("{S}", str(t.day) + suffix(t.day))


@router.get("/", response_class=JSONResponse)
async def get_bin_day(request: Request, db: Session = Depends(get_db)):
    if state.check_if_bin_date_today(db):
        return state.get_bin_info(db)
    else:
        bin_data = requests.get(BIN_URL).json()
        bin_data_list = []

        for bin in bin_data:
            bin_data_sublist = [bin["BinType"]]
            bin_date_next = datetime.strptime(bin["Next"], "%m/%d/%Y %H:%M:%S %p")
            if date.today() + timedelta(days=1) == bin_date_next.date():
                bin_data_sublist.append("Tomorrow")
                bin_data_list.insert(0, bin_data_sublist)
            elif date.today() == bin_date_next.date():
                bin_data_sublist.append("Today")
                bin_data_list.insert(0, bin_data_sublist)
            else:
                bin_data_sublist.append(custom_strftime("%b {S}", bin_date_next))
                bin_data_list.append(bin_data_sublist)

        state.set_bin_date_to_today(db)
        state.store_bin_info(db, bin_data_list)
        return bin_data_list
