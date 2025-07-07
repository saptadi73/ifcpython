from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import Form

class issueCreate(BaseModel) :
    name: str
    globalid : str
    expressid: int
    status: str
    description: str
    user_issued_id: str
    user_assign_id: Optional[str]
    project_id: str
    location: str
    date_issued: date
    closed_date: date
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        globalid : str = Form(...),
        expressid: int = Form(...),
        description: Optional[str] = Form(...),
        status: str = Form(...),
        user_issued_id: str = Form(...),
        user_assign_id: Optional[str] = Form(...),
        project_id: str = Form(...),
        location: str = Form(...),
        date_issued: date = Form(...),
        closed_date: date = Form(...),
    ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(name=name, globalid=globalid, expressid=expressid, description=description, status=status, user_issued_id=user_issued_id, user_assign_id=user_assign_id, project_id=project_id, location=location, date_issued=date_issued, closed_date=closed_date)

class issueEdit(BaseModel):
    name: Optional[str]
    globalid : Optional[str]
    expressid: Optional[int]
    description: Optional[str]
    status: Optional[str]
    user_issued_id: Optional[str]
    user_assign_id: Optional[str]
    project_id: Optional[str]
    location: Optional[str]
    date_issued: Optional[date]
    closed_date: Optional[date]
    id: str

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(...),
        globalid : Optional[str] = Form(...),
        expressid: Optional[int] = Form(...),
        description: Optional[str] = Form(...),
        status: Optional[str] = Form(...),
        user_issued_id: Optional[str] = Form(...),
        user_assign_id: Optional[str] = Form(...),
        project_id: Optional[str] = Form(...),
        location: Optional[str] = Form(...),
        date_issued: Optional[date] = Form(...),
        closed_date: Optional[date] = Form(...),
        id: str = Form(...),
    ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(name=name, globalid=globalid, expressid=expressid, description=description, status=status, user_issued_id=user_issued_id, user_assign_id=user_assign_id, project_id=project_id, location=location, date_issued=date_issued, closed_date=closed_date, id=id)

