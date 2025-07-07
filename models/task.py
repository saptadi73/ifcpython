from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import Form

class taskCreate(BaseModel) :
    name: str
    globalid : str
    expressid: int
    value: Optional[int]
    status: str
    user_issued_id: str
    user_assign_id: Optional[str]
    project_id: str
    location: str
    start_date: date
    end_date: date
    @classmethod
    def as_form(
        cls,
        name: str = Form(...),
        globalid : str = Form(...),
        expressid: int = Form(...),
        value: Optional[int] = Form(...),
        status: str = Form(...),
        user_issued_id: str = Form(...),
        user_assign_id: Optional[str] = Form(...),
        project_id: str = Form(...),
        location: str = Form(...),
        start_date: date = Form(...),
        end_date: date = Form(...),
    ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(name=name, globalid=globalid, expressid=expressid, value=value, status=status, user_issued_id=user_issued_id, user_assign_id=user_assign_id, project_id=project_id, location=location, start_date=start_date, end_date=end_date)

class taskEdit(BaseModel):
    name: Optional[str]
    globalid : Optional[str]
    expressid: Optional[int]
    value: Optional[int]
    status: Optional[str]
    user_issued_id: Optional[str]
    user_assign_id: Optional[str]
    project_id: Optional[str]
    location: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    id: str

    @classmethod
    def as_form(
        cls,
        name: Optional[str] = Form(...),
        globalid : Optional[str] = Form(...),
        expressid: Optional[int] = Form(...),
        value: Optional[int] = Form(...),
        status: Optional[str] = Form(...),
        user_issued_id: Optional[str] = Form(...),
        user_assign_id: Optional[str] = Form(...),
        project_id: Optional[str] = Form(...),
        location: Optional[str] = Form(...),
        start_date: Optional[date] = Form(...),
        end_date: Optional[date] = Form(...),
        id: str = Form(...),
    ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(name=name, globalid=globalid, expressid=expressid, value=value, status=status, user_issued_id=user_issued_id, user_assign_id=user_assign_id, project_id=project_id, location=location, start_date=start_date, end_date=end_date, id=id)

