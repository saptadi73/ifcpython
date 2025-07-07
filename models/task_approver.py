from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class taskApproverCreate(BaseModel) :
    task_id: str
    user_id : str
    urutan: Optional[int]

class taskApproverEdit(BaseModel):
    task_id: Optional[str]
    user_id : Optional[str]
    urutan: Optional[int]
    id: str

