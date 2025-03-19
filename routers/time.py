from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import (
    JSONResponse,
)

from datetime import datetime
from json import dumps

router = APIRouter(prefix="/time")


@router.get("/", response_class=JSONResponse)
async def time(request: Request):
    date_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    date_time_dict = {"datetime": date_time}
    date_time_json = dumps(date_time_dict)
    return date_time_dict


"""
Response from worldtimeapi:

{"utc_offset":"+00:00",
    "timezone":"Europe/London",
    "day_of_week":3,
    "day_of_year":78,
    "datetime":"2025-03-19T18:24:54.633442+00:00",
    "utc_datetime":"2025-03-19T18:24:54.633442+00:00",
    "unixtime":1742408694,
    "raw_offset":0,
    "week_number":12,
    "dst":false,
    "abbreviation":"GMT",
    "dst_offset":0,
    "dst_from":null,
    "dst_until":null,
    "client_ip":"206.245.202.211"
    }

app expects format "YYYY-MM-DDTHH:MM:SS"

"""
