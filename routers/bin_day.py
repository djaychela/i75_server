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


"""
Notes for someone (if API needs fixing in the future)

current API_URL is from the page at

https://online.bcpcouncil.gov.uk/bindaylookup/

Once the address is put in, you get the bin days.  If you look at network traffic in the browser dev
tools when the page loads, there is a GET request with 200 status to the needed URL:

https://online.bcpcouncil.gov.uk/bcp-apis/?api=BinDayLookup&uprn=100040763050

(my assumption is that the property is encoded in the uprn at the end, and each property is different)

The API response from BCP's site looks like this (with lots of line breaks in, so I'm assuming it's all
a bit janky!):

[
  {
    "BinType": "Food Waste",
    "PdfLink": "",
    "Communal": "false",
    "Next": "3/28/2025 12:00:00 AM",
    "Subsequent": "4/3/2025 11:00:00 PM"
  },
  {
    "BinType": "Garden Waste",
    "PdfLink": "https://www.bcpcouncil.gov.uk/gardenbincollectionsMon1",
    "Communal": "false",
    "Next": "3/24/2025 12:00:00 AM",
    "Subsequent": "4/6/2025 11:00:00 PM"
  },
  {
    "BinType": "Recycling",
    "PdfLink": "https://www.bcpcouncil.gov.uk/bincollectionbcfri1",
    "Communal": "false",
    "Next": "3/28/2025 12:00:00 AM",
    "Subsequent": "4/10/2025 11:00:00 PM"
  },
  {
    "BinType": "Rubbish",
    "PdfLink": "",
    "Communal": "false",
    "Next": "4/3/2025 11:00:00 PM",
    "Subsequent": "4/17/2025 11:00:00 PM"
  }
]

I was going to code the display to get this info directly, but thought it better for the server to do
it and hand the display something it can process simply.

So the code reformats the dates, and returns this format (for the data given above):

[["Garden Waste","Today"],["Food Waste","Mar 28th"],["Recycling","Mar 28th"],["Rubbish","Apr 3rd"]]

A list of lists, with just the bin type and date.  If the date is today or tomorrow then it is replaced with that text, which the display 
uses to change the text to red to highlight it, and placed at the front of the list.  The API serves the dates in 
an unpredictable order (in terms of dates), and I didn't code anything else to sort them.

"""