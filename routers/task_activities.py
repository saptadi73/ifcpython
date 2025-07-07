from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from services.task_activity_service import getAllTasksActivity, create_new_task_activity, delete_task_activity, edit_task_activitas, edit_task_activities_nofile
from models.task_activity import taskActivitiesCreate,taskActivitiesEdit
import os
import shutil
import time
import secrets

router = APIRouter()
UPLOAD_DIR = "uploads"

@router.get("/all/done/{id}")
def getAll():
    return getAllTasksActivity(id)


@router.post("/create")
async def create_task_activitas(task: taskActivitiesCreate = Depends(taskActivitiesCreate.as_form), file: UploadFile | None = File(None) ):

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

    return create_new_task_activity(task, random_name)

@router.post("/edit")
def update_task_activitas(task: taskActivitiesEdit = Depends(taskActivitiesEdit.as_form), file: UploadFile | None = File(None) ):
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
        return edit_task_activitas(task, random_name)
    else:
        file_path=None
        return edit_task_activities_nofile(task)

@router.post("/delete")
def hapus_task(task: taskActivitiesEdit):
    return delete_task_activity(task)
