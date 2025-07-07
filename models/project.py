from pydantic import BaseModel
from datetime import date
from typing import Optional

class projectCreate(BaseModel) :
    name: str
    description : str
    value: int
    start_date: date
    end_date: date

class projectEdit(BaseModel):
    name: Optional[str]
    description : Optional[str]
    value: Optional[int]
    start_date: Optional[date]
    end_date: Optional[date]
    id: str

