from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import Form

class taskActivitiesCreate(BaseModel) :
    activity: str
    date_activity: date
    photo: Optional[str]
    task_id: str
    user_task_activities_id: str
    @classmethod
    def as_form(
        cls,
        activity: str = Form(...),
        date_activity: date = Form(...),
        photo: Optional[str] = Form(...),
        task_id: str = Form(...),
        user_task_activities_id: str = Form(...)
        ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(activity=activity, date_activity=date_activity, photo=photo, task_id=task_id, user_task_activities_id=user_task_activities_id)

class taskActivitiesEdit(BaseModel) :
    activity: Optional[str]
    date_activity: Optional[date]
    photo: Optional[str]
    task_id: Optional[str]
    user_task_activity_id: Optional[str]
    id: str
    @classmethod
    def as_form(
        cls,
        activity: str = Form(...),
        date_activity: date = Form(...),
        photo: Optional[str] = Form(...),
        task_id: str = Form(...),
        user_task_activity_id: str = Form(...),
        id: str = Form(...)
        ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(activity=activity, date_activity=date_activity, photo=photo, task_id=task_id, user_task_activity_id=user_task_activity_id, id=id)

