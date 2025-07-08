from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi import Form

class issueActivitiesCreate(BaseModel) :
    activity: str
    date_activity: date
    photo: Optional[str]
    issue_id: str
    user_issue_activities_id: str
    @classmethod
    def as_form(
        cls,
        activity: str = Form(...),
        date_activity: date = Form(...),
        photo: Optional[str] = Form(...),
        issue_id: str = Form(...),
        user_issue_activities_id: str = Form(...)
        ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(activity=activity, date_activity=date_activity, photo=photo, issue_id=issue_id, user_issue_activities_id=user_issue_activities_id)

class issueActivitiesEdit(BaseModel) :
    activity: Optional[str]
    date_activity: Optional[date]
    photo: Optional[str]
    issue_id: Optional[str]
    user_issue_activity_id: Optional[str]
    id: str
    @classmethod
    def as_form(
        cls,
        activity: str = Form(...),
        date_activity: date = Form(...),
        photo: Optional[str] = Form(...),
        issue_id: str = Form(...),
        user_issue_activities_id: str = Form(...),
        id: str = Form(...)
        ):
        """
        Helper untuk ambil title & description dari form.
        filename nanti diisi manual setelah file di-save.
        """
        return cls(activity=activity, date_activity=date_activity, photo=photo, issue_id=issue_id, user_issue_activities_id=user_issue_activities_id, id=id)

