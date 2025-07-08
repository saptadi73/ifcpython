from fastapi import APIRouter
from services.issue_approver_service import getAllissueApprover, create_new_issue_approver, delete_issue_approver, sign_issue_approver
from models.issue_approver import issueApproverCreate,issueApproverEdit

import os
import shutil
import uuid
import time
import secrets

router = APIRouter()
UPLOAD_DIR = "uploads"

@router.get("/all/{id}")
def getAll():
    return getAllissueApprover(id)

@router.post("/create")
async def create_issue_approver(task: issueApproverCreate):
    return create_new_issue_approver(task)

@router.post("/signature")
def update_issue(task: issueApproverEdit):
    return sign_issue_approver(task)

@router.post("/delete")
def hapus_issue(task: issueApproverEdit):
    return delete_issue_approver(task)
