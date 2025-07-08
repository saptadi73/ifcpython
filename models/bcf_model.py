from pydantic import BaseModel
from datetime import date,datetime
from typing import Optional

class Markup(BaseModel) :
    Guid: Optional[str]
    Filename: Optional[str]
    Title: Optional[str]
    Priority: Optional[str]
    Status: Optional[str]
    CreationDate: Optional[str]
    CreationAuthor: Optional[str]
    ModifiedDate: Optional[datetime]
    ModifiedAuthor: Optional[str]
    AssignedTo: Optional[str]
    Description: Optional[str]
    Date: Optional[datetime]
    Author: Optional[str]
    Comment: Optional[str]

class ViewPoint(BaseModel) :
    Guid: Optional[str]
    Filename: Optional[str]
    CameraDirection_X: Optional[float]
    CameraDirection_Y: Optional[float]
    CameraDirection_Z: Optional[float]
    CameraUp_X: Optional[float]
    CameraUp_Y: Optional[float]
    CameraUp_Z: Optional[float]
    CameraPosition_X: Optional[float]
    CameraPosition_Y: Optional[float]
    CameraPosition_Z: Optional[float]

class BCFZipCreate(BaseModel) :
    Guid: Optional[str]
    Filename: Optional[str]
    FilePNGName: Optional[str]