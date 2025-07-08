from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.issue_activity_service import getAllissuesActivity, create_new_issue_activity, delete_issue_activity, edit_issue_activitas, edit_issue_activities_nofile
from models.issue_activity import issueActivitiesCreate,issueActivitiesEdit
import os
import shutil
import time
import secrets

router = APIRouter()
UPLOAD_DIR = "uploads"

@router.get("/all/done/{id}")
def getAll():
    return getAllissuesActivity(id)


@router.post("/create")
async def create_issue_activitas(task: issueActivitiesCreate = Depends(issueActivitiesCreate.as_form), file: UploadFile | None = File(None) ):

    if file:
        # ambil ekstensi file asli
        original_filename = file.filename
        _, ext = os.path.splitext(original_filename)

        random_name = f"{int(time.time())}_{secrets.token_hex(4)}{ext}"
        # path lengkap
        file_path = os.path.join(UPLOAD_DIR, random_name)
        url_photo = f"{UPLOAD_DIR}/{random_name}"

        # simpan file ke disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    else:
        file_path=None

    return create_new_issue_activity(task, random_name)

@router.post("/edit")
def update_issue_activitas(task: issueActivitiesEdit = Depends(issueActivitiesEdit.as_form), file: UploadFile | None = File(None) ):
    if file:
        # ambil ekstensi file asli
        original_filename = file.filename
        _, ext = os.path.splitext(original_filename)

        random_name = f"{int(time.time())}_{secrets.token_hex(4)}{ext}"
        # path lengkap
        file_path = os.path.join(UPLOAD_DIR, random_name)
        url_photo = f"{UPLOAD_DIR}/{random_name}"

        # simpan file ke disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return edit_issue_activitas(task, random_name)
    else:
        file_path=None
        return edit_issue_activities_nofile(task)

@router.post("/delete")
def hapus_issue(task: issueActivitiesEdit):
    return delete_issue_activity(task)
