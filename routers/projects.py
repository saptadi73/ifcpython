from fastapi import APIRouter, Depends
from services.project_service import get_all_project, create_new_project, delete_project, edit_project
from models.project import projectCreate,projectEdit

router = APIRouter()

@router.get("/all")
def getAll():
    return get_all_project()

@router.post("/create")
def create_project(project: projectCreate):
    return create_new_project(project)

@router.post("/edit")
def update_project(project: projectEdit):
    return edit_project(project)

@router.post("/delete")
def hapus_project(project: projectEdit):
    return delete_project(project)