from pydantic import BaseModel
from typing import Optional
from fastapi import Form

class issueApproverCreate(BaseModel) :
    issue_id: str
    user_id : str
    urutan: Optional[int]

class issueApproverEdit(BaseModel):
    issue_id: Optional[str]
    user_id : Optional[str]
    urutan: Optional[int]
    id: str

