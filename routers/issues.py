from fastapi import APIRouter, Depends, UploadFile, File
from services.issue_service import getAllIssueDone, create_new_issue, delete_issue, edit_issue, edit_issue_nofile,getAllIssue
from models.issue import issueCreate,issueEdit
from services.bcf_file_maker import createBCFZipFile,createMarkupFile,createViewpoinFile
from models.bcf_model import Markup, ViewPoint, BCFZipCreate

import os
import shutil
import time
import secrets

router = APIRouter()
UPLOAD_DIR = "uploads"

@router.get("/all/done/{id}")
def getAll():
    return getAllIssueDone(id)

@router.get("/all/{id}")
def getAll():
    return getAllIssue(id)

@router.post("/create")
async def create_issue(task: issueCreate = Depends(issueCreate.as_form), file: UploadFile | None = File(None) ):

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

    return create_new_issue(task, random_name)

@router.post("/edit")
def update_issue(task: issueEdit = Depends(issueEdit.as_form), file: UploadFile | None = File(None) ):
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
        return edit_issue(task, random_name)
    else:
        file_path=None
        return edit_issue_nofile(task)

@router.post("/delete")
def hapus_issue(task: issueEdit):
    return delete_issue(task)

@router.post("/bcf/markup")
def createMarkupBCF(markup: Markup) :
    return createMarkupFile(markup)

@router.post("/bcf/viewpoint")
def createViewPoint(viewpoint: ViewPoint) :
    return createViewpoinFile(viewpoint)

@router.post("/bcf/bcfzip")
def createBCFZip(bcfzip: BCFZipCreate) :
    return createBCFZipFile(bcfzip)

