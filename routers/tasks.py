from fastapi import APIRouter, Depends, UploadFile, File
from services.task_service import getAllTasksDone, create_new_task, delete_task, edit_task, edit_task_nofile,getAllTasks
from models.task import taskCreate,taskEdit

import os
import shutil
import time
import secrets

router = APIRouter()
UPLOAD_DIR = "uploads"

@router.get("/all/done/{id}")
def getAll():
    return getAllTasksDone(id)

@router.get("/all/{id}")
def getAll():
    return getAllTasks(id)

@router.post("/create")
async def create_task(task: taskCreate = Depends(taskCreate.as_form), file: UploadFile | None = File(None) ):

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

    return create_new_task(task, random_name)

@router.post("/edit")
def update_task(task: taskEdit = Depends(taskEdit.as_form), file: UploadFile | None = File(None) ):
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
        return edit_task(task, random_name)
    else:
        file_path=None
        return edit_task_nofile(task)

@router.post("/delete")
def hapus_task(task: taskEdit):
    return delete_task(task)
