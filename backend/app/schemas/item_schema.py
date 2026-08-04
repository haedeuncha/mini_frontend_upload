from datetime import datetime

from pydantic import BaseModel, Field


class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50, examples=["바지"])
    price: int = Field(ge=1, examples=[10000])
    desc: str = Field(min_length=1, max_length=200, examples=["청바지"])

class ItemPublic(BaseModel):
    id: str
    name: str
    price: int
    desc: str
    image_url: str | None = None
    image_name: str | None = None
    created_at: datetime 
    updated_at: datetime
