from pydantic import BaseModel, Field
from fastapi import Form

class ImageFile(BaseModel):
    name: str = Field(default=Form(None))


class WifiQRImageFile(BaseModel):
    ssid: str = Field(default=Form(None))
    password: str = Field(default=Form(None))