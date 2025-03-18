from pydantic import BaseModel, Field
from fastapi import Form

class ImageFile(BaseModel):
    name: str = Field(default=Form(None))