from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from dependencies import get_db
from repositories.user_repository import UserRepository
from services.user_service import UserService
from schemas.user_schema import UserCreateReqModel, UserUpdateReqModel, UserResponseModel

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db))

@router.post("/", response_model=UserResponseModel, status_code=201)
def create_user(body: UserCreateReqModel, svc: UserService = Depends(get_user_service)):
    try:
        return svc.register(body.name, body.email, body.role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UserResponseModel])
def list_users(svc: UserService = Depends(get_user_service)):
    return svc.find_all()

@router.get("/{user_id}", response_model=UserResponseModel)
def get_user(user_id: int, svc: UserService = Depends(get_user_service)):
    try:
        return svc.get(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}", response_model=UserResponseModel)
def update_user(user_id: int, body: UserUpdateReqModel,
                svc: UserService = Depends(get_user_service)):
    try:
        return svc.update(user_id, body.model_dump(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

def actor_id(x_actor_id: int = Header(...)) -> int:
    return x_actor_id

@router.delete("/{user_id}", status_code=204)
def deactivate_user(user_id: int, act_id: int = Depends(actor_id),
                    svc: UserService = Depends(get_user_service)):
    try:
        svc.deactivate(act_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{user_id}/reactivate", response_model=UserResponseModel)
def reactivate_user(user_id: int, act_id: int = Depends(actor_id),
                    svc: UserService = Depends(get_user_service)):
    try:
        return svc.reactivate(act_id, user_id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
