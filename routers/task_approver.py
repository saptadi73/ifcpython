from fastapi import APIRouter
from services.task_approver_service import getAllTaskApprover, create_new_task_approver, delete_task_approver, sign_task_approver
from models.task_approver import taskApproverCreate,taskApproverEdit

import os
import shutil
import uuid
import time
import secrets

router = APIRouter()
UPLOAD_DIR = "uploads"

@router.get("/all/{id}")
def getAll():
    return getAllTaskApprover(id)

@router.post("/create")
async def create_task_approver(task: taskApproverCreate):
    return create_new_task_approver(task)

@router.post("/signature")
def update_task(task: taskApproverEdit):
    return sign_task_approver(task)

@router.post("/delete")
def hapus_task(task: taskApproverEdit):
    return delete_task_approver(task)
