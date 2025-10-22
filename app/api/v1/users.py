# app/api/v1/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.db.session import get_db
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.api.deps import get_current_user, require_admin
from app.crud.user import create_user, list_users, get_user_by_id, update_user, delete_user

router = APIRouter()

@router.post("/", response_model=UserOut)
def create_user_endpoint(user_in: UserCreate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return create_user(db, user_in)

@router.get("/", response_model=list[UserOut])
def list_users_endpoint(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return list_users(db)

@router.get("/{user_id}", response_model=UserOut)
def get_user_endpoint(user_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if current_user.role.name != "admin" and str(current_user.id) != str(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user_endpoint(user_id: UUID, payload: UserUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if current_user.role.name != "admin" and str(current_user.id) != str(user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    update_data = payload.dict(exclude_unset=True)
    return update_user(db, user, update_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_endpoint(user_id: UUID, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    delete_user(db, user)
