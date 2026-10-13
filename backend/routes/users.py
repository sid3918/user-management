from typing import Optional

from fastapi import APIRouter, HTTPException, Query, status

import models
from schemas import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    try:
        return models.create_user(user.model_dump())
    except models.DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )



@router.get("", response_model=list[UserResponse])
def list_users(search: Optional[str] = Query(default=None, max_length=100)):
    return models.get_all_users(search)



@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    user = models.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    try:
        updated = models.update_user(user_id, user.model_dump())
    except models.DuplicateEmailError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists",
        )
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated



@router.delete("/{user_id}")
def delete_user(user_id: int):
    if not models.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}