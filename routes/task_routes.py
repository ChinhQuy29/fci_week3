from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from dependencies import get_db
from repositories.task_repository import TaskRepository
from repositories.sprint_repository import SprintRepository
from repositories.user_repository import UserRepository
from services.task_service import TaskService
from schemas.task_schema import TaskCreateReqModel, TaskAssignReqModel, TaskStatusUpdateReqModel, TaskResponseModel
import requests
from dotenv import load_dotenv
import os

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_API_ENDPOINT = os.getenv("OMDB_API_ENDPOINT")

router = APIRouter(prefix="/tasks", tags=["tasks"])

def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    return TaskService(TaskRepository(db), UserRepository(db), SprintRepository(db))

def actor_id(x_actor_id: int = Header(...)) -> int:
    return x_actor_id

@router.post("/", response_model=TaskResponseModel, status_code=201)
def create_task(body: TaskCreateReqModel, act_id: int = Depends(actor_id), svc: TaskService = Depends(get_task_service)):
    try:
        return svc.create_task(act_id, body.sprint_id, body.title, body.description, body.priority)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/sprint/{sprint_id}", response_model=list[TaskResponseModel])
def list_tasks(sprint_id: int, svc: TaskService = Depends(get_task_service)):
    return svc.find_by_sprint(sprint_id)

@router.get("/sprint/{sprint_id}/board")
def get_board(sprint_id: int, svc: TaskService = Depends(get_task_service)):
    return svc.get_board(sprint_id)

@router.get("/{task_id}", response_model=TaskResponseModel)
def get_task(task_id: int, svc: TaskService = Depends(get_task_service)):
    task = svc.find_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}/assign", response_model=TaskResponseModel)
def assign_task(task_id: int, body: TaskAssignReqModel, aid: int = Depends(actor_id),
                svc: TaskService = Depends(get_task_service)):
    try:
        return svc.assign_task(aid, task_id, body.assignee_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{task_id}/unassign", response_model=TaskResponseModel)
def unassign_task(task_id: int, aid: int = Depends(actor_id),
                  svc: TaskService = Depends(get_task_service)):
    try:
        return svc.unassign_task(aid, task_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{task_id}/start", response_model=TaskResponseModel)
def start_task(task_id: int, aid: int = Depends(actor_id),
               svc: TaskService = Depends(get_task_service)):
    try:
        return svc.start_task(aid, task_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{task_id}/finish", response_model=TaskResponseModel)
def finish_task(task_id: int, aid: int = Depends(actor_id),
                svc: TaskService = Depends(get_task_service)):
    try:
        return svc.finish_task(aid, task_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{task_id}/status", response_model=TaskResponseModel)
def update_status(task_id: int, body: TaskStatusUpdateReqModel,
                  aid: int = Depends(actor_id),
                  svc: TaskService = Depends(get_task_service)):
    try:
        return svc.transition_task(aid, task_id, body.status)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[TaskResponseModel])
def list_all_tasks(svc: TaskService = Depends(get_task_service)):
    return svc.get_all_tasks()

@router.post("/movie", response_model=TaskResponseModel)
def create_task_from_movie(aid: int = Depends(actor_id), svc: TaskService = Depends(get_task_service)):
    sprint_id = 1
    response = requests.get(f"{OMDB_API_ENDPOINT}?apikey={OMDB_API_KEY}&t=Dune")
    data = response.json()
    try:
        return svc.create_task(aid, sprint_id, data["Title"], data["Genre"])
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
