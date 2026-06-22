from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from dependencies import get_db
from repositories.sprint_repository import SprintRepository
from repositories.user_repository import UserRepository
from services.sprint_service import SprintService
from schemas.sprint_schema import SprintAddMemberReqModel, SprintCreateReqModel, SprintResponseModel, SprintWithTaskResponseModel

router = APIRouter(prefix="/sprints", tags=["sprints"])

def get_sprint_service(db: Session = Depends(get_db)) -> SprintService:
    return SprintService(SprintRepository(db), UserRepository(db))

def actor_id(x_actor_id: int = Header(...)) -> int:
    return x_actor_id

@router.post("/", response_model = SprintResponseModel, status_code=201)
def create_sprint(body: SprintCreateReqModel, act_id: int = Depends(actor_id), svc: SprintService = Depends(get_sprint_service)):
    try:
        return svc.create_sprint(act_id, body.title, body.from_date, body.to_date)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[SprintResponseModel])
def list_sprints(svc: SprintService = Depends(get_sprint_service)):
    return svc.find_all()

@router.get("/{sprint_id}", response_model=SprintResponseModel)
def get_sprint(sprint_id: int, svc: SprintService = Depends(get_sprint_service)):
    sprint = svc.find_by_id(sprint_id)
    if not sprint:
        raise HTTPException(status_code=404, detail="Sprint not found")
    return sprint

@router.post("/{sprint_id}", response_model=SprintResponseModel)
def add_member(sprint_id: int, body: SprintAddMemberReqModel, svc: SprintService = Depends(get_sprint_service), act_id: int = Depends(actor_id)):
    try:
        return svc.add_member(act_id, body.user_id, sprint_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{sprint_id}/activate", response_model=SprintResponseModel)
def activate_sprint(sprint_id: int, svc: SprintService = Depends(get_sprint_service), act_id: int = Depends(actor_id)):
    try:
        return svc.activate_sprint(act_id, sprint_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{sprint_id}/close", response_model=SprintResponseModel)
def close_sprint(sprint_id: int, svc: SprintService = Depends(get_sprint_service), act_id: int = Depends(actor_id)):
    try:
        return svc.close_sprint(act_id, sprint_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{sprint_id}/tasks-with-member", response_model=SprintWithTaskResponseModel)
def get_all_tasks_with_member(sprint_id: int, svc: SprintService = Depends(get_sprint_service)):
    return svc.get_all_tasks_with_corresponding_member(sprint_id)